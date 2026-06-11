import 'package:flutter/material.dart';
import '../../../core/ui/widgets.dart';
import '../../../core/ui/theme.dart';

class CalendarScreen extends StatefulWidget {
  const CalendarScreen({Key? key}) : super(key: key);

  @override
  State<CalendarScreen> createState() => _CalendarScreenState();
}

class _CalendarScreenState extends State<CalendarScreen> {
  late DateTime _selectedDate;

  @override
  void initState() {
    super.initState();
    _selectedDate = DateTime.now();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.floraWhite,
      appBar: FloralAppBar(title: 'Calendar'),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Month/Year selector
            FloralCard(
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      IconButton(
                        icon: Icon(Icons.chevron_left),
                        onPressed: () {},
                      ),
                      Text(
                        'June 2024',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      IconButton(
                        icon: Icon(Icons.chevron_right),
                        onPressed: () {},
                      ),
                    ],
                  ),
                  SizedBox(height: 16),
                  // Calendar Grid
                  _CalendarGrid(),
                ],
              ),
            ),
            SizedBox(height: 24),

            // Events for selected date
            Text('Events for June 11',
                style: Theme.of(context).textTheme.titleLarge),
            SizedBox(height: 12),
            _EventItem(
              time: '09:00 AM',
              title: 'Team Meeting',
              duration: '1 hour',
              color: AppTheme.primaryPink,
            ),
            SizedBox(height: 8),
            _EventItem(
              time: '02:00 PM',
              title: 'Yoga Session',
              duration: '1 hour',
              color: AppTheme.floraGreen,
            ),
            SizedBox(height: 8),
            _EventItem(
              time: '05:30 PM',
              title: 'Dinner with friends',
              duration: '2 hours',
              color: AppTheme.floraPeach,
            ),
            SizedBox(height: 24),

            // Add Event Button
            SizedBox(
              width: double.infinity,
              child: FloralButton(
                label: '+ Add Event',
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

class _CalendarGrid extends StatelessWidget {
  final List<String> weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  final List<int> dates = List.generate(30, (i) => i + 1);

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Week days header
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: weekDays
              .map((day) => Text(
                    day,
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: AppTheme.mediumText,
                    ),
                  ))
              .toList(),
        ),
        SizedBox(height: 12),
        // Calendar dates
        GridView.builder(
          shrinkWrap: true,
          physics: NeverScrollableScrollPhysics(),
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 7,
            childAspectRatio: 1,
            mainAxisSpacing: 8,
            crossAxisSpacing: 8,
          ),
          itemCount: 35,
          itemBuilder: (context, index) {
            int day = index - 3 + 1;
            bool isCurrentMonth = day > 0 && day <= 30;
            bool isSelected = isCurrentMonth && day == 11;

            return Container(
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isSelected
                    ? AppTheme.primaryPink
                    : isCurrentMonth
                        ? AppTheme.palePink
                        : Colors.transparent,
              ),
              child: Center(
                child: isCurrentMonth
                    ? Text(
                        '$day',
                        style: TextStyle(
                          color: isSelected ? Colors.white : AppTheme.darkText,
                          fontWeight: isSelected ? FontWeight.bold : null,
                        ),
                      )
                    : SizedBox.shrink(),
              ),
            );
          },
        ),
      ],
    );
  }
}

class _EventItem extends StatelessWidget {
  final String time;
  final String title;
  final String duration;
  final Color color;

  const _EventItem({
    required this.time,
    required this.title,
    required this.duration,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return FloralCard(
      child: Row(
        children: [
          Container(
            width: 4,
            height: 60,
            decoration: BoxDecoration(
              color: color,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                SizedBox(height: 4),
                Row(
                  children: [
                    Icon(Icons.access_time, size: 14, color: AppTheme.lightText),
                    SizedBox(width: 4),
                    Text(
                      '$time • $duration',
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                  ],
                ),
              ],
            ),
          ),
          Icon(Icons.chevron_right, color: AppTheme.lightText),
        ],
      ),
    );
  }
}
