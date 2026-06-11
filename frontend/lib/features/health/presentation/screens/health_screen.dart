import 'package:flutter/material.dart';
import '../../../core/ui/widgets.dart';
import '../../../core/ui/theme.dart';

class HealthScreen extends StatefulWidget {
  const HealthScreen({Key? key}) : super(key: key);

  @override
  State<HealthScreen> createState() => _HealthScreenState();
}

class _HealthScreenState extends State<HealthScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.floraWhite,
      appBar: FloralAppBar(title: 'Health Tracker'),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Water Intake
            Text('Water Intake', style: Theme.of(context).textTheme.titleLarge),
            SizedBox(height: 12),
            FloralCard(
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: List.generate(8, (index) {
                      bool filled = index < 6;
                      return Column(
                        children: [
                          Container(
                            width: 40,
                            height: 40,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: filled
                                  ? AppTheme.lightPink
                                  : AppTheme.palePink,
                            ),
                            child: Icon(
                              Icons.water_drop,
                              color: filled
                                  ? Colors.white
                                  : AppTheme.lightText,
                            ),
                          ),
                          SizedBox(height: 4),
                          Text('${index + 1}',
                              style: Theme.of(context).textTheme.bodySmall),
                        ],
                      );
                    }),
                  ),
                  SizedBox(height: 16),
                  Text('6 of 8 glasses consumed',
                      style: Theme.of(context).textTheme.bodyMedium),
                ],
              ),
            ),
            SizedBox(height: 24),

            // Sleep Tracking
            Text('Sleep', style: Theme.of(context).textTheme.titleLarge),
            SizedBox(height: 12),
            FloralCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('Last Night',
                              style: Theme.of(context).textTheme.titleSmall),
                          SizedBox(height: 8),
                          Text('7h 30m',
                              style: Theme.of(context)
                                  .textTheme
                                  .displaySmall
                                  ?.copyWith(
                                    fontSize: 24,
                                    color: AppTheme.primaryPink,
                                  )),
                        ],
                      ),
                      Icon(Icons.bedtime, size: 48, color: AppTheme.floraPurple),
                    ],
                  ),
                  SizedBox(height: 16),
                  FloralProgressIndicator(
                    value: 0.9375,
                    label: 'Goal: 8 hours',
                    color: AppTheme.floraPurple,
                  ),
                ],
              ),
            ),
            SizedBox(height: 24),

            // Mood Tracking
            Text('Mood', style: Theme.of(context).textTheme.titleLarge),
            SizedBox(height: 12),
            FloralCard(
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      _MoodOption(emoji: '😢', label: 'Bad'),
                      _MoodOption(emoji: '😐', label: 'Okay'),
                      _MoodOption(emoji: '🙂', label: 'Good', selected: true),
                      _MoodOption(emoji: '😄', label: 'Great'),
                      _MoodOption(emoji: '😍', label: 'Amazing'),
                    ],
                  ),
                  SizedBox(height: 16),
                  Text('Current Mood: Great',
                      style: Theme.of(context).textTheme.bodyMedium),
                ],
              ),
            ),
            SizedBox(height: 24),

            // Menstrual Cycle
            Text('Menstrual Cycle',
                style: Theme.of(context).textTheme.titleLarge),
            SizedBox(height: 12),
            FloralCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Next Period in 7 days',
                      style: Theme.of(context).textTheme.titleMedium),
                  SizedBox(height: 12),
                  FloralProgressIndicator(
                    value: 0.6,
                    label: 'Current Cycle',
                    color: AppTheme.primaryPink,
                  ),
                ],
              ),
            ),
            SizedBox(height: 24),

            // Add Button
            SizedBox(
              width: double.infinity,
              child: FloralButton(
                label: '+ Log Health Entry',
                onPressed: () {},
                icon: Icons.add,
              ),
            ),
            SizedBox(height: 16),
          ],
        ),
      ),
    );
  }
}

class _MoodOption extends StatelessWidget {
  final String emoji;
  final String label;
  final bool selected;

  const _MoodOption({
    required this.emoji,
    required this.label,
    this.selected = false,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          width: 50,
          height: 50,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: selected ? AppTheme.lightPink : AppTheme.palePink,
          ),
          child: Center(
            child: Text(emoji, style: TextStyle(fontSize: 28)),
          ),
        ),
        SizedBox(height: 6),
        Text(label, style: Theme.of(context).textTheme.bodySmall),
      ],
    );
  }
}
