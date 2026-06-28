# DearMe Database Guide

## Overview

DearMe uses PostgreSQL as the primary transactional database. The schema is designed to support user accounts, health tracking, productivity, journaling, placement preparation, AI memory, notifications, analytics, and squad-based engagement.

## Core tables

- users: application users and authentication anchors.
- user_profiles: personal profile details and roll number storage.
- user_preferences: UI and notification preferences.
- user_settings: generic key/value settings for feature flags and small configuration data.
- auth_accounts: authentication provider connections.

## Feature tables

- water_goals / water_logs: hydration tracking.
- sleep_scores / sleep_logs: sleep quality and duration tracking.
- period_cycles / period_predictions / period_symptoms: menstrual health tracking.
- mood_logs: mood entries.
- journal_entries / journal_tags / journal_entry_tags: journaling and tagging.
- goals / goal_milestones / goal_progress: goal tracking.
- tasks / task_reminders / task_comments: productivity tracking.
- calendar_events / event_participants: scheduling.
- applications / assessments / interviews: placement tracking.
- notifications / notification_templates / notification_logs: reminders and delivery status.
- ai_memories / ai_recommendations / ai_conversations: AI context and recommendations.
- daily_metrics / weekly_metrics / monthly_metrics / life_scores: analytics.

## Important constraints

- UUID primary keys are used throughout.
- Soft-delete support is provided via `deleted_at` on major tables.
- One-to-one user profile data is enforced where applicable.
- CHECK constraints exist for metrics and rating fields.

## Indexes

Key indexes support dashboard queries, task lookups, goal lookups, notification lookups, and analytics searches.

## Materialized views

- mv_life_scores
- mv_daily_summary
- mv_weekly_summary
- mv_monthly_summary
- mv_productivity_summary

## Notes

The schema is designed to be normalized and production-friendly. The Alembic migration in this repository captures the latest database enhancements so deployments can stay consistent.
