import 'package:flutter/material.dart';

class FloatingMascot extends StatefulWidget {
  final double size;
  const FloatingMascot({Key? key, this.size = 84}) : super(key: key);

  @override
  State<FloatingMascot> createState() => _FloatingMascotState();
}

class _FloatingMascotState extends State<FloatingMascot> with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(seconds: 5))..repeat(reverse: true);
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
        final dy = 6 * sin(_ctrl.value * 2 * 3.14159);
        return Transform.translate(
          offset: Offset(0, dy),
          child: Container(
            width: widget.size,
            height: widget.size,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              gradient: const LinearGradient(colors: [Color(0xFFFFE6EE), Color(0xFFFFCFE6)]),
              boxShadow: [BoxShadow(color: Colors.pink.shade100.withOpacity(0.4), blurRadius: 12, spreadRadius: 1)],
            ),
            child: const Icon(Icons.person, color: Colors.white, size: 40),
          ),
        );
      },
    );
  }
}
