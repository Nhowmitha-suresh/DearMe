import 'package:flutter/material.dart';
import '../../../core/ui/widgets.dart';
import '../../../core/ui/theme.dart';

class TasksScreen extends StatefulWidget {
  const TasksScreen({Key? key}) : super(key: key);

  @override
  State<TasksScreen> createState() => _TasksScreenState();
}

class _TasksScreenState extends State<TasksScreen> {
  final List<Task> tasks = [
    Task(
      title: 'Complete project proposal',
      priority: 'High',
      dueDate: 'Today',
      completed: false,
    ),
    Task(
      title: 'Review team feedback',
      priority: 'Medium',
      dueDate: 'Tomorrow',
      completed: true,
    ),
    Task(
      title: 'Update portfolio',
      priority: 'Medium',
      dueDate: 'This Week',
      completed: false,
    ),
    Task(
      title: 'Schedule meeting',
      priority: 'Low',
      dueDate: 'This Week',
      completed: false,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    final completedCount = tasks.where((t) => t.completed).length;

    return Scaffold(
      backgroundColor: AppTheme.floraWhite,
      appBar: FloralAppBar(title: 'Tasks'),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: Icon(Icons.add),
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Progress Overview
            FloralCard(
              showGradient: true,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Tasks Progress',
                          style: Theme.of(context)
                              .textTheme
                              .titleMedium
                              ?.copyWith(color: Colors.white)),
                      SizedBox(height: 8),
                      Text('$completedCount/${tasks.length} completed',
                          style: Theme.of(context)
                              .textTheme
                              .bodyMedium
                              ?.copyWith(color: Colors.white70)),
                    ],
                  ),
                  Stack(
                    alignment: Alignment.center,
                    children: [
                      SizedBox(
                        width: 80,
                        height: 80,
                        child: CircularProgressIndicator(
                          value: completedCount / tasks.length,
                          strokeWidth: 6,
                          backgroundColor: Colors.white30,
                          valueColor:
                              AlwaysStoppedAnimation(Colors.white),
                        ),
                      ),
                      Text(
                        '${((completedCount / tasks.length) * 100).toStringAsFixed(0)}%',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            SizedBox(height: 24),

            // Filters
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  _FilterChip(label: 'All', selected: true),
                  SizedBox(width: 8),
                  _FilterChip(label: 'High Priority'),
                  SizedBox(width: 8),
                  _FilterChip(label: 'Today'),
                  SizedBox(width: 8),
                  _FilterChip(label: 'Completed'),
                ],
              ),
            ),
            SizedBox(height: 20),

            // Tasks List
            Text('All Tasks', style: Theme.of(context).textTheme.titleLarge),
            SizedBox(height: 12),
            ListView.builder(
              shrinkWrap: true,
              physics: NeverScrollableScrollPhysics(),
              itemCount: tasks.length,
              itemBuilder: (context, index) {
                final task = tasks[index];
                return _TaskCard(task: task);
              },
            ),
            SizedBox(height: 16),
          ],
        ),
      ),
    );
  }
}

class Task {
  final String title;
  final String priority;
  final String dueDate;
  bool completed;

  Task({
    required this.title,
    required this.priority,
    required this.dueDate,
    required this.completed,
  });
}

class _TaskCard extends StatefulWidget {
  final Task task;

  const _TaskCard({required this.task});

  @override
  State<_TaskCard> createState() => _TaskCardState();
}

class _TaskCardState extends State<_TaskCard> {
  @override
  Widget build(BuildContext context) {
    return FloralCard(
      child: Row(
        children: [
          Checkbox(
            value: widget.task.completed,
            onChanged: (value) {
              setState(() => widget.task.completed = value ?? false);
            },
            activeColor: AppTheme.primaryPink,
          ),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  widget.task.title,
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        decoration: widget.task.completed
                            ? TextDecoration.lineThrough
                            : null,
                        color: widget.task.completed
                            ? AppTheme.lightText
                            : null,
                      ),
                ),
                SizedBox(height: 4),
                Row(
                  children: [
                    _PriorityBadge(priority: widget.task.priority),
                    SizedBox(width: 8),
                    Icon(Icons.access_time, size: 14, color: AppTheme.lightText),
                    SizedBox(width: 4),
                    Text(widget.task.dueDate,
                        style: Theme.of(context).textTheme.bodySmall),
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

class _PriorityBadge extends StatelessWidget {
  final String priority;

  const _PriorityBadge({required this.priority});

  @override
  Widget build(BuildContext context) {
    Color color;
    switch (priority.toLowerCase()) {
      case 'high':
        color = Color(0xFFD32F2F);
        break;
      case 'medium':
        color = AppTheme.floraPeach;
        break;
      default:
        color = AppTheme.floraGreen;
    }

    return Container(
      padding: EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      decoration: BoxDecoration(
        color: color.withOpacity(0.2),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Text(
        priority,
        style: TextStyle(
          fontSize: 11,
          fontWeight: FontWeight.bold,
          color: color,
        ),
      ),
    );
  }
}

class _FilterChip extends StatelessWidget {
  final String label;
  final bool selected;

  const _FilterChip({required this.label, this.selected = false});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: selected ? AppTheme.primaryPink : AppTheme.palePink,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: selected ? Colors.white : AppTheme.darkText,
          fontWeight: FontWeight.w500,
          fontSize: 12,
        ),
      ),
    );
  }
}
