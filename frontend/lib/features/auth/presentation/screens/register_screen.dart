import 'package:flutter/material.dart';
import '../../../core/ui/widgets.dart';
import '../../../core/ui/theme.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({Key? key}) : super(key: key);

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _nameController;
  late TextEditingController _emailController;
  late TextEditingController _passwordController;
  late TextEditingController _confirmPasswordController;

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController();
    _emailController = TextEditingController();
    _passwordController = TextEditingController();
    _confirmPasswordController = TextEditingController();
  }

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
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
              height: 200,
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
                    SizedBox(height: 12),
                    Text(
                      'Create Your Account',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            // Registration Form
            Padding(
              padding: EdgeInsets.all(24),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    SizedBox(height: 16),
                    FloralTextField(
                      label: 'Full Name',
                      hint: 'Enter your full name',
                      controller: _nameController,
                      prefixIcon: Icons.person,
                      validator: (value) {
                        if (value?.isEmpty ?? true) return 'Name is required';
                        return null;
                      },
                    ),
                    SizedBox(height: 16),
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
                        if ((value?.length ?? 0) < 6) {
                          return 'Password must be at least 6 characters';
                        }
                        return null;
                      },
                    ),
                    SizedBox(height: 16),
                    FloralTextField(
                      label: 'Confirm Password',
                      hint: 'Confirm your password',
                      controller: _confirmPasswordController,
                      obscureText: true,
                      prefixIcon: Icons.lock,
                      suffixIcon: Icons.visibility,
                      validator: (value) {
                        if (value?.isEmpty ?? true) {
                          return 'Please confirm password';
                        }
                        if (value != _passwordController.text) {
                          return 'Passwords do not match';
                        }
                        return null;
                      },
                    ),
                    SizedBox(height: 24),
                    SizedBox(
                      width: double.infinity,
                      child: FloralButton(
                        label: 'Create Account',
                        onPressed: () {
                          if (_formKey.currentState!.validate()) {
                            // TODO: Implement registration logic
                          }
                        },
                      ),
                    ),
                    SizedBox(height: 16),
                    Center(
                      child: RichText(
                        text: TextSpan(
                          text: 'Already have an account? ',
                          style: TextStyle(color: Colors.black),
                          children: [
                            TextSpan(
                              text: 'Login',
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
