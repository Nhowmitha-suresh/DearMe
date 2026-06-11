import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../core/ui/widgets.dart';
import '../../../core/ui/theme.dart';
import '../../../core/router.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _selectedIndex = 0;

  final List<FloralBottomNavItem> navItems = [
    FloralBottomNavItem(icon: Icons.home, label: 'Home'),
    FloralBottomNavItem(icon: Icons.favorite, label: 'Health'),
    FloralBottomNavItem(icon: Icons.task_alt, label: 'Tasks'),
    FloralBottomNavItem(icon: Icons.flag, label: 'Goals'),
    FloralBottomNavItem(icon: Icons.more_horiz, label: 'More'),
  ];

  void _onNavTap(int index) {
    setState(() => _selectedIndex = index);
    switch (index) {
      case 0:
        break; // Stay on home
      case 1:
        context.go(AppRouter.health);
        break;
      case 2:
        context.go(AppRouter.tasks);
        break;
      case 3:
        context.go(AppRouter.goals);
        break;
      case 4:
        _showMoreMenu();
        break;
    }
  }

  void _showMoreMenu() {
    showModalBottomSheet(
      context: context,
      backgroundColor: AppTheme.floraWhite,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            height: 4,
            width: 40,
            margin: EdgeInsets.symmetric(vertical: 12),
            decoration: BoxDecoration(
              color: AppTheme.palePink,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          ListTile(
            leading: Icon(Icons.edit, color: AppTheme.primaryPink),
            title: Text('Journal'),
            onTap: () {
              Navigator.pop(context);
              context.go(AppRouter.journal);
            },
          ),
          ListTile(
            leading: Icon(Icons.calendar_today, color: AppTheme.primaryPink),
            title: Text('Calendar'),
            onTap: () {
              Navigator.pop(context);
              context.go(AppRouter.calendar);
            },
          ),
          ListTile(
            leading: Icon(Icons.psychology, color: AppTheme.primaryPink),
            title: Text('AI Companion'),
            onTap: () {
              Navigator.pop(context);
              context.go(AppRouter.aiCompanion);
            },
          ),
          SizedBox(height: 16),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.floraWhite,
      appBar: FloralAppBar(
        title: 'Dashboard',
        actions: [
          IconButton(
            icon: Icon(Icons.notifications, color: Colors.white),
            onPressed: () {},
          ),
          IconButton(
            icon: Icon(Icons.person, color: Colors.white),
            onPressed: () {},
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Welcome Section
            FloralCard(
              showGradient: true,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Good Morning, Sarah',
                    style: Theme.of(context)
                        .textTheme
                        .headlineMedium
                        ?.copyWith(color: Colors.white),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'You\'re doing great! Keep pushing forward.',
                    style: Theme.of(context)
                        .textTheme
                        .bodyMedium
                        ?.copyWith(color: Colors.white70),
                  ),
                ],
              ),
            ),
            SizedBox(height: 24),

            // Quick Stats
            Text('Today\'s Overview',
                style: Theme.of(context).textTheme.titleLarge),
            SizedBox(height: 12),
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: NeverScrollableScrollPhysics(),
              childAspectRatio: 1.2,
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
              children: [
                FloralStatCard(
                  label: 'Tasks Done',
                  value: '6/10',
                  icon: Icons.check_circle,
                  iconColor: AppTheme.floraGreen,
                ),
                FloralStatCard(
                  label: 'Mood Score',
                  value: '8.5',
                  icon: Icons.sentiment_satisfied,
                  iconColor: AppTheme.floraPeach,
                ),
                FloralStatCard(
                  label: 'Water Intake',
                  value: '6/8 L',
                  icon: Icons.water_drop,
                  iconColor: AppTheme.lightPink,
                ),
                FloralStatCard(
                  label: 'Sleep',
                  value: '7h 30m',
                  icon: Icons.bedtime,
                  iconColor: AppTheme.floraPurple,
                ),
              ],
            ),
            SizedBox(height: 24),

            // Quick Actions
            Text('Quick Actions',
                style: Theme.of(context).textTheme.titleLarge),
            SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: FloralCard(
                    onTap: () => context.go(AppRouter.journal),
                    child: Column(
                      children: [
                        Icon(Icons.edit, size: 32, color: AppTheme.primaryPink),
                        SizedBox(height: 8),
                        Text('Journal',
                            style: Theme.of(context).textTheme.titleSmall,
                            textAlign: TextAlign.center),
                      ],
                    ),
                  ),
                ),
                SizedBox(width: 12),
                Expanded(
                  child: FloralCard(
                    onTap: () => context.go(AppRouter.aiCompanion),
                    child: Column(
                      children: [
                        Icon(Icons.psychology,
                            size: 32, color: AppTheme.primaryPink),
                        SizedBox(height: 8),
                        Text('Chat with AI',
                            style: Theme.of(context).textTheme.titleSmall,
                            textAlign: TextAlign.center),
                      ],
                    ),
                  ),
                ),
                SizedBox(width: 12),
                Expanded(
                  child: FloralCard(
                    onTap: () => context.go(AppRouter.calendar),
                    child: Column(
                      children: [
                        Icon(Icons.calendar_today,
                            size: 32, color: AppTheme.primaryPink),
                        SizedBox(height: 8),
                        Text('Calendar',
                            style: Theme.of(context).textTheme.titleSmall,
                            textAlign: TextAlign.center),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            SizedBox(height: 24),

            // Progress Section
            Text('This Week\'s Progress',
                style: Theme.of(context).textTheme.titleLarge),
            SizedBox(height: 12),
            FloralCard(
              child: Column(
                children: [
                  FloralProgressIndicator(
                    value: 0.75,
                    label: 'Tasks Completed',
                  ),
                  SizedBox(height: 16),
                  FloralProgressIndicator(
                    value: 0.6,
                    label: 'Goals Progress',
                    color: AppTheme.floraPeach,
                  ),
                  SizedBox(height: 16),
                  FloralProgressIndicator(
                    value: 0.85,
                    label: 'Health Check-ins',
                    color: AppTheme.floraGreen,
                  ),
                ],
              ),
            ),
            SizedBox(height: 24),
          ],
        ),
      ),
      bottomNavigationBar: FloralBottomNavBar(
        currentIndex: _selectedIndex,
        onTap: _onNavTap,
        items: navItems,
      ),
    );
  }
}
