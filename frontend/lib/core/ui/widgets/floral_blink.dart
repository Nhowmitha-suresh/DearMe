import 'package:flutter/material.dart';

class FloralBlink extends StatefulWidget {
  final double size;
  const FloralBlink({Key? key, this.size = 160}) : super(key: key);

  @override
  State<FloralBlink> createState() => _FloralBlinkState();
}

class _FloralBlinkState extends State<FloralBlink> with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _opacity;
  late final Animation<double> _scale;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: const Duration(seconds: 2))..repeat(reverse: true);
    _opacity = Tween<double>(begin: 0.6, end: 1.0).animate(CurvedAnimation(parent: _controller, curve: Curves.easeInOut));
    _scale = Tween<double>(begin: 0.95, end: 1.06).animate(CurvedAnimation(parent: _controller, curve: Curves.easeInOut));
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Opacity(
          opacity: _opacity.value,
          child: Transform.scale(
            scale: _scale.value,
            child: CustomPaint(
              size: Size(widget.size, widget.size),
              painter: _FloralPainter(),
            ),
          ),
        );
      },
    );
  }
}

class _FloralPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final paint = Paint()..style = PaintingStyle.fill;

    // petals
    for (int i = 0; i < 6; i++) {
      final angle = i * (360 / 6) * 3.14159 / 180;
      final petalCenter = Offset(center.dx + (size.width * 0.22) * cos(angle), center.dy + (size.height * 0.22) * sin(angle));
      paint.color = Color.lerp(const Color(0xFFFFCFE6), const Color(0xFFFFE6EE), i / 6)!.withOpacity(0.95);
      canvas.drawOval(Rect.fromCenter(center: petalCenter, width: size.width * 0.38, height: size.height * 0.22), paint);
    }

    // core
    paint.color = const Color(0xFFFF8FB3);
    canvas.drawCircle(center, size.width * 0.14, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
