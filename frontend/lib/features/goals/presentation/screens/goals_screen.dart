import 'package:flutter/material.dart';
import '../../../core/ui/widgets.dart';
import '../../../core/ui/theme.dart';

class GoalsScreen extends StatefulWidget {
  const GoalsScreen({Key? key}) : super(key: key);

  @override
  State<GoalsScreen> createState() => _GoalsScreenState();
}

class _GoalsScreenState extends State<GoalsScreen> {
  final List<Goal> goals = [
    Goal(
      title: 'Complete Flutter Course',
      category: 'Learning',
      progress: 0.65,
      daysLeft: 45,
      color: AppTheme.floraPurple,
    ),
    Goal(
      title: 'Read 12 Books',
      category: 'Personal',
      progress: 0.42,
      daysLeft: 120,
      color: AppTheme.floraGreen,
    ),
    Goal(
      title: 'Exercise 3x Weekly',
      category: 'Health',
      progress: 0.78,
      daysLeft: 90,
      color: AppTheme.floraPeach,
    ),
    Goal(
      title: 'Build a Startup',
      category: 'Career',
      progress: 0.33,
      daysLeft: 180,
      color: AppTheme.roseGold,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.floraWhite,
      appBar: FloralAppBar(title: 'Goals'),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: Icon(Icons.add),
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Stats Overview
            Row(
              children: [
                Expanded(
                  child: FloralStatCard(
                    label: 'Active Goals',
                    value: '${goals.length}',
                    icon: Icons.flag,
                  ),
                ),
                SizedBox(width: 12),
                Expanded(
                  child: FloralStatCard(
                    label: 'On Track',
                    value: '4',
                    icon: Icons.trending_up,
                    iconColor: AppTheme.floraGreen,
                  ),
                ),
              ],
            ),
            SizedBox(height: 24),

            // Goals List
            Text('Your Goals', style: Theme.of(context).textTheme.titleLarge),
            SizedBox(height: 12),
            ListView.builder(
              shrinkWrap: true,
              physics: NeverScrollableScrollPhysics(),
              itemCount: goals.length,
              itemBuilder: (context, index) {
                final goal = goals[index];
                return _GoalCard(goal: goal);
              },
            ),
            SizedBox(height: 24),

            // Goal Tips
            Text('Goal Tips', style: Theme.of(context).textTheme.titleLarge),
            SizedBox(height: 12),
            FloralCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _TipItem(
                    title: 'Break It Down',
                    description: 'Divide large goals into smaller milestones',
                  ),
                  SizedBox(height: 12),
                  Divider(color: AppTheme.dividerColor),
                  SizedBox(height: 12),
                  _TipItem(
                    title: 'Track Progress',
                    description: 'Update your goals regularly to stay motivated',
                  ),
                  SizedBox(height: 12),
                  Divider(color: AppTheme.dividerColor),
                  SizedBox(height: 12),
                  _TipItem(
                    title: 'Celebrate Wins',
                    description: 'Acknowledge milestones you achieve',
                  ),
                ],
              ),
            ),
            SizedBox(height: 16),
          ],
        ),
      ),
    );
  }
}

class Goal {
  final String title;
  final String category;
  final double progress;
  final int daysLeft;
  final Color color;

  Goal({
    required this.title,
    required this.category,
    required this.progress,
    required this.daysLeft,
    required this.color,
  });
}

class _GoalCard extends StatelessWidget {
  final Goal goal;

  const _GoalCard({required this.goal});

  @override
  Widget build(BuildContext context) {
    return FloralCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      goal.title,
                      style: Theme.of(context).textTheme.titleMedium,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    SizedBox(height: 4),
                    Container(
                      padding:
                          EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                      decoration: BoxDecoration(
                        color: goal.color.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Text(
                        goal.category,
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                          color: goal.color,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(width: 12),
              Stack(
                alignment: Alignment.center,
                children: [
                  SizedBox(
                    width: 60,
                    height: 60,
                    child: CircularProgressIndicator(
                      value: goal.progress,
                      strokeWidth: 4,
                      backgroundColor: goal.color.withOpacity(0.2),
                      valueColor:
                          AlwaysStoppedAnimation(goal.color),
                    ),
                  ),
                  Text(
                    '${(goal.progress * 100).toStringAsFixed(0)}%',
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      color: goal.color,
                    ),
                  ),
                ],
              ),
            ],
          ),
          SizedBox(height: 12),
          Row(
            children: [
              Icon(Icons.calendar_today, size: 16, color: AppTheme.lightText),
              SizedBox(width: 6),
              Text(
                '${goal.daysLeft} days left',
                style: Theme.of(context).textTheme.bodySmall,
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _TipItem extends StatelessWidget {
  final String title;
  final String description;

  const _TipItem({required this.title, required this.description});

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: 24,
          height: 24,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: AppTheme.lightPink,
          ),
          child: Icon(Icons.check, size: 14, color: Colors.white),
        ),
        SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: Theme.of(context).textTheme.titleSmall,
              ),
              SizedBox(height: 2),
              Text(
                description,
                style: Theme.of(context).textTheme.bodySmall,
              ),
            ],
          ),
        ),
      ],
    );
  }
}
