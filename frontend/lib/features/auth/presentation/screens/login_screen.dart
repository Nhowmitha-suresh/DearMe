import 'package:flutter/material.dart';
import '../../../core/ui/widgets.dart';
import '../../../core/ui/theme.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _emailController;
  late TextEditingController _passwordController;

  @override
  void initState() {
    super.initState();
    _emailController = TextEditingController();
    _passwordController = TextEditingController();
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.floraWhite,
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Header with gradient
            Container(
              height: 250,
              decoration: BoxDecoration(
                gradient: AppTheme.flowerGradient,
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(40),
                  bottomRight: Radius.circular(40),
                ),
              ),
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.favorite, size: 48, color: Colors.white),
                    SizedBox(height: 16),
                    Text(
                      'DearMe',
                      style: TextStyle(
                        fontSize: 36,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Welcome Back',
                      style: TextStyle(
                        fontSize: 16,
                        color: Colors.white70,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            // Login Form
            Padding(
              padding: EdgeInsets.all(24),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    SizedBox(height: 24),
                    FloralTextField(
                      label: 'Email',
                      hint: 'Enter your email',
                      controller: _emailController,
                      keyboardType: TextInputType.emailAddress,
                      prefixIcon: Icons.email,
                      validator: (value) {
                        if (value?.isEmpty ?? true) return 'Email is required';
                        return null;
                      },
                    ),
                    SizedBox(height: 16),
                    FloralTextField(
                      label: 'Password',
                      hint: 'Enter your password',
                      controller: _passwordController,
                      obscureText: true,
                      prefixIcon: Icons.lock,
                      suffixIcon: Icons.visibility,
                      validator: (value) {
                        if (value?.isEmpty ?? true) return 'Password is required';
                        return null;
                      },
                    ),
                    SizedBox(height: 8),
                    Align(
                      alignment: Alignment.centerRight,
                      child: TextButton(
                        onPressed: () {},
                        child: Text('Forgot Password?'),
                      ),
                    ),
                    SizedBox(height: 24),
                    SizedBox(
                      width: double.infinity,
                      child: FloralButton(
                        label: 'Login',
                        onPressed: () {
                          if (_formKey.currentState!.validate()) {
                            // TODO: Implement login logic
                          }
                        },
                      ),
                    ),
                    SizedBox(height: 16),
                    Center(
                      child: RichText(
                        text: TextSpan(
                          text: "Don't have an account? ",
                          style: TextStyle(color: Colors.black),
                          children: [
                            TextSpan(
                              text: 'Register',
                              style: TextStyle(
                                color: AppTheme.primaryPink,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
