import 'package:flutter/material.dart';
import '../../../core/ui/widgets.dart';
import '../../../core/ui/theme.dart';

class JournalScreen extends StatefulWidget {
  const JournalScreen({Key? key}) : super(key: key);

  @override
  State<JournalScreen> createState() => _JournalScreenState();
}

class _JournalScreenState extends State<JournalScreen> {
  final List<JournalEntry> entries = [
    JournalEntry(
      date: 'Today',
      mood: 'Happy',
      title: 'Great day at work!',
      preview:
          'Finished the project ahead of schedule. Feeling accomplished and proud of the team.',
    ),
    JournalEntry(
      date: 'Yesterday',
      mood: 'Peaceful',
      title: 'Evening reflection',
      preview: 'Had a wonderful yoga session. Feeling centered and calm.',
    ),
    JournalEntry(
      date: '2 days ago',
      mood: 'Motivated',
      title: 'New goals set',
      preview: 'Planning for the next quarter. Excited about new opportunities.',
    ),
    JournalEntry(
      date: '3 days ago',
      mood: 'Grateful',
      title: 'Friends gathering',
      preview: 'Spent time with close friends. Grateful for their support.',
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.floraWhite,
      appBar: FloralAppBar(title: 'Journal'),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: Icon(Icons.add),
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Quote of the Day
            FloralCard(
              showGradient: true,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Quote of the Day',
                    style: Theme.of(context)
                        .textTheme
                        .titleSmall
                        ?.copyWith(color: Colors.white70),
                  ),
                  SizedBox(height: 12),
                  Text(
                    '"The only way out is through." - Robert Frost',
                    style: Theme.of(context)
                        .textTheme
                        .bodyMedium
                        ?.copyWith(
                          color: Colors.white,
                          fontStyle: FontStyle.italic,
                        ),
                  ),
                ],
              ),
            ),
            SizedBox(height: 24),

            // Entries List
            Text('Your Entries', style: Theme.of(context).textTheme.titleLarge),
            SizedBox(height: 12),
            ListView.builder(
              shrinkWrap: true,
              physics: NeverScrollableScrollPhysics(),
              itemCount: entries.length,
              itemBuilder: (context, index) {
                final entry = entries[index];
                return _JournalEntryCard(entry: entry);
              },
            ),
            SizedBox(height: 16),
          ],
        ),
      ),
    );
  }
}

class JournalEntry {
  final String date;
  final String mood;
  final String title;
  final String preview;

  JournalEntry({
    required this.date,
    required this.mood,
    required this.title,
    required this.preview,
  });
}

class _JournalEntryCard extends StatelessWidget {
  final JournalEntry entry;

  const _JournalEntryCard({required this.entry});

  @override
  Widget build(BuildContext context) {
    return FloralCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                entry.date,
                style: Theme.of(context).textTheme.titleSmall,
              ),
              Container(
                padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: AppTheme.palePink,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  entry.mood,
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    color: AppTheme.primaryPink,
                  ),
                ),
              ),
            ],
          ),
          SizedBox(height: 8),
          Text(
            entry.title,
            style: Theme.of(context).textTheme.titleMedium,
          ),
          SizedBox(height: 8),
          Text(
            entry.preview,
            style: Theme.of(context).textTheme.bodySmall,
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
          SizedBox(height: 12),
          Align(
            alignment: Alignment.centerRight,
            child: TextButton(
              onPressed: () {},
              child: Text('Read More'),
            ),
          ),
        ],
      ),
    );
  }
}
