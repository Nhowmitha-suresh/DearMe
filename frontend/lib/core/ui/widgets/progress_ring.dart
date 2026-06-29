import 'package:flutter/material.dart';
import 'package:percent_indicator/circular_percent_indicator.dart';

class AnimatedProgressRing extends StatelessWidget {
  final double percent;
  final double size;
  final String label;
  const AnimatedProgressRing({Key? key, required this.percent, this.size = 120, this.label = ''}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return CircularPercentIndicator(
      radius: size / 2,
      lineWidth: 12.0,
      percent: percent.clamp(0.0, 1.0),
      center: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text('${(percent * 100).toInt()}%', style: const TextStyle(fontWeight: FontWeight.bold)),
          if (label.isNotEmpty) Text(label, style: const TextStyle(fontSize: 12)),
        ],
      ),
      progressColor: const Color(0xFFFF8FB3),
      backgroundColor: const Color(0xFFFFE6EE),
      circularStrokeCap: CircularStrokeCap.round,
      animation: true,
      animationDuration: 800,
    );
  }
}
