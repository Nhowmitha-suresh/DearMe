import 'dart:math';
import 'package:flutter/material.dart';

class Butterfly extends StatefulWidget {
  final double size;
  const Butterfly({Key? key, this.size = 80}) : super(key: key);

  @override
  State<Butterfly> createState() => _ButterflyState();
}

class _ButterflyState extends State<Butterfly> with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(seconds: 4))..repeat();
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _ctrl,
      builder: (context, child) {
        final t = _ctrl.value;
        final dx = 40 * sin(t * 2 * pi);
        final dy = -10 * cos(t * 4 * pi);
        final rotation = 0.25 * sin(t * 2 * pi);
        return Transform.translate(
          offset: Offset(dx, dy),
          child: Transform.rotate(
            angle: rotation,
            child: SizedBox(
              width: widget.size,
              height: widget.size,
              child: CustomPaint(painter: _ButterflyPainter(t)),
            ),
          ),
        );
      },
    );
  }
}

class _ButterflyPainter extends CustomPainter {
  final double t;
  _ButterflyPainter(this.t);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..style = PaintingStyle.fill;
    final center = Offset(size.width / 2, size.height / 2);
    // left wing
    paint.color = Color.lerp(const Color(0xFFFFA3C4), const Color(0xFFFFD7EB), t)!;
    final lPath = Path();
    lPath.moveTo(center.dx, center.dy);
    lPath.quadraticBezierTo(center.dx - size.width * 0.7, center.dy - size.height * 0.9 * (0.6 + 0.4 * sin(t * pi)), center.dx - size.width * 0.1, center.dy - size.height * 0.05);
    lPath.quadraticBezierTo(center.dx - size.width * 0.4, center.dy + size.height * 0.7, center.dx, center.dy);
    canvas.drawPath(lPath, paint);

    // right wing
    paint.color = Color.lerp(const Color(0xFFFFE6EE), const Color(0xFFFFCFE6), 1 - t)!;
    final rPath = Path();
    rPath.moveTo(center.dx, center.dy);
    rPath.quadraticBezierTo(center.dx + size.width * 0.7, center.dy - size.height * 0.9 * (0.6 + 0.4 * cos(t * pi)), center.dx + size.width * 0.1, center.dy - size.height * 0.05);
    rPath.quadraticBezierTo(center.dx + size.width * 0.4, center.dy + size.height * 0.7, center.dx, center.dy);
    canvas.drawPath(rPath, paint);

    // body
    final bodyPaint = Paint()..color = const Color(0xFF6B4353);
    canvas.drawRect(Rect.fromCenter(center: center, width: size.width * 0.08, height: size.height * 0.4), bodyPaint);
  }

  @override
  bool shouldRepaint(covariant _ButterflyPainter oldDelegate) => oldDelegate.t != t;
}
