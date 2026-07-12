from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
import uuid
from datetime import datetime


from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.finance import Expense, SavingsGoal
from app.schemas.finance import (
    ExpenseCreate,
    ExpenseRead,
    SavingsGoalCreate,
    SavingsGoalRead,
    FinanceSummary,
    CategorySpend
)

router = APIRouter(prefix='/finance', tags=['finance'])


@router.post('/expenses', response_model=ExpenseRead, summary='Log a new expense')
async def create_expense(payload: ExpenseCreate, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    expense = Expense(
        user_id=user.id,
        amount=payload.amount,
        category=payload.category,
        description=payload.description,
        logged_at=payload.logged_at or datetime.utcnow()
    )
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense


@router.get('/expenses', response_model=List[ExpenseRead], summary='Get user expense history')
async def get_expenses(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    q = select(Expense).where(
        Expense.user_id == user.id,
        Expense.is_deleted == False
    ).order_by(Expense.logged_at.desc())
    res = await db.execute(q)
    return res.scalars().all()


@router.post('/savings', response_model=SavingsGoalRead, summary='Set a savings goal')
async def create_savings_goal(payload: SavingsGoalCreate, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    goal = SavingsGoal(
        user_id=user.id,
        title=payload.title,
        target_amount=payload.target_amount,
        current_amount=payload.current_amount or 0.0,
        target_date=payload.target_date
    )
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal


@router.get('/savings', response_model=List[SavingsGoalRead], summary='Get user savings goals')
async def get_savings_goals(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    q = select(SavingsGoal).where(
        SavingsGoal.user_id == user.id,
        SavingsGoal.is_deleted == False
    )
    res = await db.execute(q)
    return res.scalars().all()


@router.put('/savings/{goal_id}', response_model=SavingsGoalRead, summary='Update savings progress')
async def update_savings_progress(goal_id: uuid.UUID, current_amount: float, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    q = select(SavingsGoal).where(
        SavingsGoal.id == goal_id,
        SavingsGoal.user_id == user.id,
        SavingsGoal.is_deleted == False
    )
    res = await db.execute(q)
    goal = res.scalars().first()
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Savings goal not found')
    
    goal.current_amount = current_amount
    await db.commit()
    await db.refresh(goal)
    return goal


@router.get('/summary', response_model=FinanceSummary, summary='Get finance dashboard summary')
async def get_finance_summary(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    # 1. Total expenses
    exp_q = select(func.coalesce(func.sum(Expense.amount), 0.0)).where(
        Expense.user_id == user.id,
        Expense.is_deleted == False
    )
    exp_res = await db.execute(exp_q)
    total_expenses = float(exp_res.scalar_one())

    # 2. Category spending breakdown
    breakdown_q = select(
        Expense.category,
        func.sum(Expense.amount)
    ).where(
        Expense.user_id == user.id,
        Expense.is_deleted == False
    ).group_by(Expense.category)
    
    breakdown_res = await db.execute(breakdown_q)
    breakdown = []
    for cat, total in breakdown_res.all():
        breakdown.append(CategorySpend(category=cat, total=float(total)))

    # 3. Savings goals list
    savings_q = select(SavingsGoal).where(
        SavingsGoal.user_id == user.id,
        SavingsGoal.is_deleted == False
    )
    savings_res = await db.execute(savings_q)
    savings = savings_res.scalars().all()

    return FinanceSummary(
        total_expenses=total_expenses,
        category_breakdown=breakdown,
        savings_progress=savings
    )
