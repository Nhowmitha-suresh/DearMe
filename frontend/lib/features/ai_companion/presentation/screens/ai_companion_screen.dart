import 'package:flutter/material.dart';
import '../../../core/ui/widgets.dart';
import '../../../core/ui/theme.dart';

class AiCompanionScreen extends StatefulWidget {
  const AiCompanionScreen({Key? key}) : super(key: key);

  @override
  State<AiCompanionScreen> createState() => _AiCompanionScreenState();
}

class _AiCompanionScreenState extends State<AiCompanionScreen> {
  late TextEditingController _messageController;
  final List<ChatMessage> messages = [
    ChatMessage(
      text: 'Hi! I\'m your AI companion. How can I help you today?',
      isUser: false,
    ),
    ChatMessage(
      text: 'I\'ve been feeling stressed about work lately.',
      isUser: true,
    ),
    ChatMessage(
      text:
          'I understand. Work-related stress is common. Would you like to talk about what\'s causing it? Sometimes sharing helps.',
      isUser: false,
    ),
  ];

  @override
  void initState() {
    super.initState();
    _messageController = TextEditingController();
  }

  @override
  void dispose() {
    _messageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.floraWhite,
      appBar: FloralAppBar(
        title: 'AI Companion',
        actions: [
          IconButton(
            icon: Icon(Icons.info_outline, color: Colors.white),
            onPressed: () {},
          ),
        ],
      ),
      body: Column(
        children: [
          // Chat messages
          Expanded(
            child: ListView.builder(
              padding: EdgeInsets.all(16),
              itemCount: messages.length,
              itemBuilder: (context, index) {
                final message = messages[index];
                return _ChatBubble(message: message);
              },
            ),
          ),

          // Input area
          Container(
            padding: EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [
                BoxShadow(
                  color: AppTheme.primaryPink.withOpacity(0.08),
                  blurRadius: 8,
                  offset: Offset(0, -2),
                ),
              ],
            ),
            child: Row(
              children: [
                Expanded(
                  child: Container(
                    decoration: BoxDecoration(
                      color: AppTheme.palePink,
                      borderRadius: BorderRadius.circular(24),
                    ),
                    child: TextField(
                      controller: _messageController,
                      decoration: InputDecoration(
                        hintText: 'Type your message...',
                        border: InputBorder.none,
                        contentPadding: EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 12,
                        ),
                      ),
                    ),
                  ),
                ),
                SizedBox(width: 8),
                FloatingActionButton(
                  mini: true,
                  onPressed: () {
                    if (_messageController.text.isNotEmpty) {
                      setState(() {
                        messages.add(ChatMessage(
                          text: _messageController.text,
                          isUser: true,
                        ));
                        _messageController.clear();
                      });
                    }
                  },
                  child: Icon(Icons.send),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class ChatMessage {
  final String text;
  final bool isUser;

  ChatMessage({required this.text, required this.isUser});
}

class _ChatBubble extends StatelessWidget {
  final ChatMessage message;

  const _ChatBubble({required this.message});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(bottom: 12),
      child: Row(
        mainAxisAlignment:
            message.isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        children: [
          if (!message.isUser) ...[
            Container(
              width: 32,
              height: 32,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: AppTheme.flowerGradient,
              ),
              child: Icon(Icons.psychology, size: 16, color: Colors.white),
            ),
            SizedBox(width: 8),
          ],
          Flexible(
            child: Container(
              padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: message.isUser ? AppTheme.lightPink : AppTheme.palePink,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Text(
                message.text,
                style: TextStyle(
                  color: message.isUser ? Colors.white : AppTheme.darkText,
                  fontSize: 14,
                ),
              ),
            ),
          ),
          if (message.isUser) SizedBox(width: 8),
        ],
      ),
    );
  }
}
