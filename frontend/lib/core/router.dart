import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../features/auth/presentation/screens/login_screen.dart';
import '../features/auth/presentation/screens/register_screen.dart';
import '../features/dashboard/presentation/screens/dashboard_screen.dart';
import '../features/health/presentation/screens/health_screen.dart';
import '../features/tasks/presentation/screens/tasks_screen.dart';
import '../features/goals/presentation/screens/goals_screen.dart';
import '../features/journal/presentation/screens/journal_screen.dart';
import '../features/calendar/presentation/screens/calendar_screen.dart';
import '../features/ai_companion/presentation/screens/ai_companion_screen.dart';

class AppRouter {
  static const String splash = '/';
  static const String login = '/login';
  static const String register = '/register';
  static const String dashboard = '/dashboard';
  static const String health = '/health';
  static const String tasks = '/tasks';
  static const String goals = '/goals';
  static const String journal = '/journal';
  static const String calendar = '/calendar';
  static const String aiCompanion = '/ai-companion';

  static final GoRouter router = GoRouter(
    initialLocation: dashboard,
    routes: [
      GoRoute(
        path: login,
        builder: (context, state) => LoginScreen(),
      ),
      GoRoute(
        path: register,
        builder: (context, state) => RegisterScreen(),
      ),
      GoRoute(
        path: dashboard,
        builder: (context, state) => DashboardScreen(),
      ),
      GoRoute(
        path: health,
        builder: (context, state) => HealthScreen(),
      ),
      GoRoute(
        path: tasks,
        builder: (context, state) => TasksScreen(),
      ),
      GoRoute(
        path: goals,
        builder: (context, state) => GoalsScreen(),
      ),
      GoRoute(
        path: journal,
        builder: (context, state) => JournalScreen(),
      ),
      GoRoute(
        path: calendar,
        builder: (context, state) => CalendarScreen(),
      ),
      GoRoute(
        path: aiCompanion,
        builder: (context, state) => AiCompanionScreen(),
      ),
    ],
  );
}
