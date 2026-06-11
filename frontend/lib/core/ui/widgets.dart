import 'package:flutter/material.dart';
import '../ui/theme.dart';

/// Floral Card Widget with pink theme
class FloralCard extends StatelessWidget {
  final Widget child;
  final EdgeInsetsGeometry padding;
  final VoidCallback? onTap;
  final Color? backgroundColor;
  final bool showGradient;

  const FloralCard({
    Key? key,
    required this.child,
    this.padding = const EdgeInsets.all(16),
    this.onTap,
    this.backgroundColor,
    this.showGradient = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    Widget content = Padding(
      padding: padding,
      child: child,
    );

    if (showGradient) {
      content = Container(
        decoration: BoxDecoration(
          gradient: AppTheme.softFlowerGradient,
          borderRadius: BorderRadius.circular(16),
        ),
        child: content,
      );
    }

    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Container(
          decoration: BoxDecoration(
            color: backgroundColor ?? Colors.white,
            borderRadius: BorderRadius.circular(16),
            boxShadow: [
              BoxShadow(
                color: AppTheme.primaryPink.withOpacity(0.08),
                blurRadius: 12,
                offset: Offset(0, 4),
              ),
            ],
          ),
          child: content,
        ),
      ),
    );
  }
}

/// Custom App Bar with pink floral theme
class FloralAppBar extends StatelessWidget implements PreferredSizeWidget {
  final String title;
  final List<Widget>? actions;
  final Widget? leading;
  final VoidCallback? onBackPressed;
  final bool showGradient;

  const FloralAppBar({
    Key? key,
    required this.title,
    this.actions,
    this.leading,
    this.onBackPressed,
    this.showGradient = true,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: showGradient ? AppTheme.flowerGradient : null,
        color: showGradient ? null : AppTheme.floraWhite,
        boxShadow: [
          BoxShadow(
            color: AppTheme.lightPink.withOpacity(0.1),
            blurRadius: 8,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: leading ??
            (Navigator.canPop(context)
                ? IconButton(
                    icon: Icon(Icons.arrow_back, color: Colors.white),
                    onPressed: onBackPressed ?? () => Navigator.pop(context),
                  )
                : null),
        title: Text(
          title,
          style: TextStyle(
            color: Colors.white,
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
        actions: actions,
      ),
    );
  }

  @override
  Size get preferredSize => Size.fromHeight(56);
}

/// Floral Button with pink theme
class FloralButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;
  final bool isOutlined;
  final IconData? icon;
  final bool isLoading;

  const FloralButton({
    Key? key,
    required this.label,
    required this.onPressed,
    this.isOutlined = false,
    this.icon,
    this.isLoading = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    if (isOutlined) {
      return OutlinedButton.icon(
        onPressed: isLoading ? null : onPressed,
        icon: icon != null ? Icon(icon) : SizedBox.shrink(),
        label: isLoading
            ? SizedBox(
                height: 20,
                width: 20,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  valueColor:
                      AlwaysStoppedAnimation(AppTheme.primaryPink),
                ),
              )
            : Text(label),
      );
    }

    return ElevatedButton.icon(
      onPressed: isLoading ? null : onPressed,
      icon: icon != null ? Icon(icon) : SizedBox.shrink(),
      label: isLoading
          ? SizedBox(
              height: 20,
              width: 20,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                valueColor: AlwaysStoppedAnimation(Colors.white),
              ),
            )
          : Text(label),
    );
  }
}

/// Floral Text Field
class FloralTextField extends StatefulWidget {
  final String label;
  final String? hint;
  final TextEditingController? controller;
  final TextInputType keyboardType;
  final bool obscureText;
  final IconData? prefixIcon;
  final IconData? suffixIcon;
  final VoidCallback? onSuffixIconPressed;
  final String? Function(String?)? validator;
  final int? maxLines;
  final int? minLines;

  const FloralTextField({
    Key? key,
    required this.label,
    this.hint,
    this.controller,
    this.keyboardType = TextInputType.text,
    this.obscureText = false,
    this.prefixIcon,
    this.suffixIcon,
    this.onSuffixIconPressed,
    this.validator,
    this.maxLines = 1,
    this.minLines,
  }) : super(key: key);

  @override
  State<FloralTextField> createState() => _FloralTextFieldState();
}

class _FloralTextFieldState extends State<FloralTextField> {
  late bool _obscureText;

  @override
  void initState() {
    super.initState();
    _obscureText = widget.obscureText;
  }

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: widget.controller,
      keyboardType: widget.keyboardType,
      obscureText: _obscureText,
      maxLines: widget.obscureText ? 1 : widget.maxLines,
      minLines: widget.minLines,
      validator: widget.validator,
      decoration: InputDecoration(
        labelText: widget.label,
        hintText: widget.hint,
        prefixIcon: widget.prefixIcon != null ? Icon(widget.prefixIcon) : null,
        suffixIcon: widget.suffixIcon != null
            ? IconButton(
                icon: Icon(widget.suffixIcon),
                onPressed: () {
                  if (widget.obscureText) {
                    setState(() => _obscureText = !_obscureText);
                  } else {
                    widget.onSuffixIconPressed?.call();
                  }
                },
              )
            : null,
      ),
    );
  }
}

/// Floral Bottom Navigation Bar
class FloralBottomNavBar extends StatelessWidget {
  final int currentIndex;
  final Function(int) onTap;
  final List<FloralBottomNavItem> items;

  const FloralBottomNavBar({
    Key? key,
    required this.currentIndex,
    required this.onTap,
    required this.items,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        boxShadow: [
          BoxShadow(
            color: AppTheme.primaryPink.withOpacity(0.1),
            blurRadius: 12,
            offset: Offset(0, -2),
          ),
        ],
      ),
      child: BottomNavigationBar(
        currentIndex: currentIndex,
        onTap: onTap,
        type: BottomNavigationBarType.fixed,
        items: items
            .map((item) => BottomNavigationBarItem(
                  icon: Icon(item.icon),
                  label: item.label,
                ))
            .toList(),
      ),
    );
  }
}

class FloralBottomNavItem {
  final IconData icon;
  final String label;

  FloralBottomNavItem({required this.icon, required this.label});
}

/// Floral Progress Indicator
class FloralProgressIndicator extends StatelessWidget {
  final double value; // 0.0 to 1.0
  final String label;
  final Color? color;

  const FloralProgressIndicator({
    Key? key,
    required this.value,
    required this.label,
    this.color,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: Theme.of(context).textTheme.titleMedium),
            Text('${(value * 100).toStringAsFixed(0)}%',
                style: Theme.of(context).textTheme.titleSmall),
          ],
        ),
        SizedBox(height: 8),
        ClipRRect(
          borderRadius: BorderRadius.circular(12),
          child: LinearProgressIndicator(
            value: value,
            minHeight: 8,
            backgroundColor: AppTheme.palePink,
            valueColor:
                AlwaysStoppedAnimation(color ?? AppTheme.primaryPink),
          ),
        ),
      ],
    );
  }
}

/// Floral Stat Card
class FloralStatCard extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;
  final Color? iconColor;

  const FloralStatCard({
    Key? key,
    required this.label,
    required this.value,
    required this.icon,
    this.iconColor,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FloralCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: iconColor ?? AppTheme.primaryPink, size: 28),
          SizedBox(height: 12),
          Text(label, style: Theme.of(context).textTheme.titleSmall),
          SizedBox(height: 4),
          Text(value,
              style: Theme.of(context).textTheme.displaySmall?.copyWith(
                    fontSize: 20,
                    color: AppTheme.primaryPink,
                  )),
        ],
      ),
    );
  }
}
