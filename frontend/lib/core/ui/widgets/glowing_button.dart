import 'package:flutter/material.dart';

class GlowingButton extends StatefulWidget {
  final Widget child;
  final VoidCallback onTap;
  const GlowingButton({Key? key, required this.child, required this.onTap}) : super(key: key);

  @override
  State<GlowingButton> createState() => _GlowingButtonState();
}

class _GlowingButtonState extends State<GlowingButton> with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(seconds: 2))..repeat(reverse: true);
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: widget.onTap,
      child: AnimatedBuilder(
        animation: _ctrl,
        builder: (context, child) {
          final glow = 6 + 6 * _ctrl.value;
          return Container(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
            decoration: BoxDecoration(
              color: const Color(0xFFFFCFE6),
              borderRadius: BorderRadius.circular(14),
              boxShadow: [
                BoxShadow(color: const Color(0xFFFFA3C4).withOpacity(0.4), blurRadius: glow, spreadRadius: 1),
              ],
            ),
            child: widget.child,
          );
        },
      ),
    );
  }
}
