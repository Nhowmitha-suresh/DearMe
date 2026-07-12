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
                  child: Transform.rotate(
                    angle: -0.05, // Subtle italic skew
                    child: Text(
                      'N',
                      style: TextStyle(
                        fontFamily: 'Outfit',
                        fontSize: widget.size * 0.52,
                        fontWeight: FontWeight.w900,
                        fontStyle: FontStyle.italic,
                        letterSpacing: -2,
                        foreground: Paint()
                          ..shader = const LinearGradient(
                            colors: [
                              Color(0xFFE0F7FA),
                              Color(0xFF80DEEA),
                              Color(0xFF26C6DA),
                              Color(0xFF00ACC1),
                            ],
                            begin: Alignment.topCenter,
                            end: Alignment.bottomCenter,
                          ).createShader(Rect.fromLTWH(0, 0, widget.size, widget.size)),
                        shadows: [
                          Shadow(
                            color: Colors.black.withOpacity(0.4),
                            offset: const Offset(2, 2),
                            blurRadius: 4,
                          ),
                          Shadow(
                            color: const Color(0xFF00E5FF).withOpacity(0.5),
                            offset: const Offset(0, 0),
                            blurRadius: 10,
                          ),
                        ],
                      ),
                    ),
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
