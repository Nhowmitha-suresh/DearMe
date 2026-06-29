import 'dart:math';
import 'package:flutter/material.dart';

class FloatingPetals extends StatefulWidget {
  final int count;
  final double width;
  const FloatingPetals({Key? key, this.count = 8, this.width = 300}) : super(key: key);

  @override
  State<FloatingPetals> createState() => _FloatingPetalsState();
}

class _FloatingPetalsState extends State<FloatingPetals> with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(seconds: 6))..repeat();
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.width,
      height: widget.width,
      child: AnimatedBuilder(
        animation: _ctrl,
        builder: (context, child) {
          return CustomPaint(
            painter: _PetalPainter(progress: _ctrl.value, count: widget.count),
          );
        },
      ),
    );
  }
}

class _PetalPainter extends CustomPainter {
  final double progress;
  final int count;
  _PetalPainter({required this.progress, required this.count});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final rand = Random(42);
    for (int i = 0; i < count; i++) {
      final angle = (i / count) * 2 * pi + progress * 2 * pi * (0.5 + rand.nextDouble());
      final radius = size.width * (0.18 + 0.22 * sin(progress * 2 * pi + i));
      final petalCenter = center + Offset(cos(angle) * radius, sin(angle) * radius);
      final paint = Paint()..color = Color.lerp(const Color(0xFFFFCFE6), const Color(0xFFFFE6EE), i / count)!.withOpacity(0.9 - 0.3 * (i / count));
      canvas.drawOval(Rect.fromCenter(center: petalCenter, width: size.width * 0.28, height: size.height * 0.12), paint);
    }
  }

  @override
  bool shouldRepaint(covariant _PetalPainter old) => old.progress != progress;
}
