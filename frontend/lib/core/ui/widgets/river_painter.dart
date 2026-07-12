import 'dart:math' as math;
import 'package:flutter/material.dart';

class RiverFlowWidget extends StatefulWidget {
  final double flowRate;     // Speed multiplier (e.g. 0.5 to 2.0)
  final double clarity;      // Clarity percentage (0.0 to 1.0)
  final double height;       // Canvas height

  const RiverFlowWidget({
    Key? key,
    this.flowRate = 1.0,
    this.clarity = 1.0,
    this.height = 200.0,
  }) : super(key: key);

  @override
  State<RiverFlowWidget> createState() => _RiverFlowWidgetState();
}

class _RiverFlowWidgetState extends State<RiverFlowWidget> with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 10),
    )..repeat();
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
        return CustomPaint(
          size: Size(double.infinity, widget.height),
          painter: RiverFlowPainter(
            animationValue: _controller.value,
            flowRate: widget.flowRate,
            clarity: widget.clarity,
          ),
        );
      },
    );
  }
}

class RiverFlowPainter extends CustomPainter {
  final double animationValue;
  final double flowRate;
  final double clarity;

  RiverFlowPainter({
    required this.animationValue,
    required this.flowRate,
    required this.clarity,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final width = size.width;
    final height = size.height;

    // Define colors based on clarity.
    // Clean water is vibrant cyan/teal; murky water has gray/brown tones mixed in.
    final Color riverBaseColor = Color.lerp(
      const Color(0xFFC0D6DF), // Murky gray-blue
      const Color(0xFF0077B6), // Vibrant deep water blue
      clarity,
    )!;

    final Color riverWave1Color = Color.lerp(
      const Color(0xFF8E9AAF), // Murky wave
      const Color(0xFF00B4D8).withOpacity(0.7), // Mid-tone active blue
      clarity,
    )!;

    final Color riverWave2Color = Color.lerp(
      const Color(0xFFD8E2DC),
      const Color(0xFF90E0EF).withOpacity(0.5), // High light aqua blue
      clarity,
    )!;

    final basePaint = Paint()
      ..color = riverBaseColor
      ..style = PaintStyle.fill;

    // Draw solid base river background
    canvas.drawRect(Rect.fromLTWH(0, 0, width, height), basePaint);

    // Draw Wave 1 (Mid-depth wave flowing right)
    final wave1Paint = Paint()
      ..color = riverWave1Color
      ..style = PaintStyle.fill;

    final path1 = Path();
    path1.moveTo(0, height);
    for (double x = 0; x <= width; x++) {
      // Flow rate speeds up the phase animation
      final phase = animationValue * 2 * math.pi * flowRate;
      final y = height * 0.45 +
          math.sin(x * 0.015 + phase) * 12 +
          math.cos(x * 0.008 + phase * 0.5) * 6;
      path1.lineTo(x, y);
    }
    path1.lineTo(width, height);
    path1.close();
    canvas.drawPath(path1, wave1Paint);

    // Draw Wave 2 (Top surface wave flowing slightly faster)
    final wave2Paint = Paint()
      ..color = riverWave2Color
      ..style = PaintStyle.fill;

    final path2 = Path();
    path2.moveTo(0, height);
    for (double x = 0; x <= width; x++) {
      final phase = animationValue * 2 * math.pi * flowRate * 1.4 + 2.0;
      final y = height * 0.6 +
          math.sin(x * 0.02 + phase) * 8 +
          math.sin(x * 0.01 + phase * 0.8) * 4;
      path2.lineTo(x, y);
    }
    path2.lineTo(width, height);
    path2.close();
    canvas.drawPath(path2, wave2Paint);

    // Draw little details like sparkles/river foam lines
    final foamPaint = Paint()
      ..color = Colors.white.withOpacity(0.2 + (0.3 * clarity))
      ..style = PaintStyle.stroke
      ..strokeWidth = 2.0;

    final path3 = Path();
    for (double x = 20; x < width - 20; x += 60) {
      final phase = animationValue * 2 * math.pi * flowRate * 1.1 + x;
      final y = height * 0.52 + math.sin(x + phase) * 4;
      path3.moveTo(x, y);
      path3.quadraticBezierTo(x + 15, y - 2, x + 30, y + math.cos(phase)*2);
    }
    canvas.drawPath(path3, foamPaint);
  }

  @override
  bool shouldRepaint(covariant RiverFlowPainter oldDelegate) {
    return oldDelegate.animationValue != animationValue ||
        oldDelegate.flowRate != flowRate ||
        oldDelegate.clarity != clarity;
  }
}
