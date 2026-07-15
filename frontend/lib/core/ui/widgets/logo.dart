import 'dart:math' as math;
import 'package:flutter/material.dart';

class NadhiLogo extends StatefulWidget {
  final double size;
  final bool animate;

  const NadhiLogo({
    Key? key,
    this.size = 120.0,
    this.animate = true,
  }) : super(key: key);

  @override
  State<NadhiLogo> createState() => _NadhiLogoState();
}

class _NadhiLogoState extends State<NadhiLogo> with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 4),
    );
    if (widget.animate) {
      _controller.repeat();
    }
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
        return Container(
          width: widget.size,
          height: widget.size,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            gradient: const LinearGradient(
              colors: [Color(0xFF003B46), Color(0xFF07575B)],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            boxShadow: [
              BoxShadow(
                color: const Color(0xFF00ACC1).withOpacity(0.3 + 0.1 * math.sin(_controller.value * 2 * math.pi)),
                blurRadius: 20 + 5 * math.sin(_controller.value * 2 * math.pi),
                spreadRadius: 2,
              ),
            ],
            border: Border.all(
              color: const Color(0xFF80DEEA).withOpacity(0.4),
              width: 2.0,
            ),
          ),
          child: ClipOval(
            child: Stack(
              children: [
                // Inner water ripple effect
                Positioned.fill(
                  child: CustomPaint(
                    painter: _LogoRipplePainter(
                      animationValue: _controller.value,
                    ),
                  ),
                ),
                // Stylized Italic N
                Center(
                  child: Image.asset(
                    'assets/images/logo.png',
                    width: widget.size * 0.8,
                    height: widget.size * 0.8,
                    fit: BoxFit.contain,
                    errorBuilder: (context, error, stackTrace) {
                      return const Icon(
                        Icons.image_not_supported,
                        color: Colors.white54,
                      );
                    },
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}

class _LogoRipplePainter extends CustomPainter {
  final double animationValue;

  _LogoRipplePainter({required this.animationValue});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = const Color(0xFF00E5FF).withOpacity(0.12)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    final center = Offset(size.width / 2, size.height / 2);
    final maxRadius = size.width / 2;

    for (int i = 0; i < 3; i++) {
      final t = (animationValue + i / 3.0) % 1.0;
      final radius = maxRadius * t;
      paint.color = const Color(0xFF00E5FF).withOpacity(0.15 * (1.0 - t));
      canvas.drawCircle(center, radius, paint);
    }
  }

  @override
  bool shouldRepaint(covariant _LogoRipplePainter oldDelegate) {
    return oldDelegate.animationValue != animationValue;
  }
}
