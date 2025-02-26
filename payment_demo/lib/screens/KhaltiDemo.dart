import 'package:flutter/material.dart';
import 'package:khalti_checkout_flutter/khalti_checkout_flutter.dart';
import 'dart:developer';

class KhaltiSDKDemo extends StatefulWidget {
  const KhaltiSDKDemo({super.key, required this.pidx});
  final String pidx;
  @override
  State<KhaltiSDKDemo> createState() => _KhaltiSDKDemoState();
}

class _KhaltiSDKDemoState extends State<KhaltiSDKDemo> {
  late final Future<Khalti?> khalti;

  String pidx =
      'ZyzCEMLFz2QYFYfERGh8LE'; // Should be generated via a server-side POST request.

  PaymentResult? paymentResult;

  @override
  void initState() {
    super.initState();
    final payConfig = KhaltiPayConfig(
      publicKey:
          '43617c95ade94e7c9747148bff335956', // This is a dummy public key for example purpose
      pidx: widget.pidx,
      environment: Environment.test,
    );

    khalti = Khalti.init(
      enableDebugging: true,
      payConfig: payConfig,
      onPaymentResult: (paymentResult, khalti) {
        log(paymentResult.toString());
        setState(() {
          this.paymentResult = paymentResult;
        });
        khalti.close(context);
      },
      onMessage: (
        khalti, {
        description,
        statusCode,
        event,
        needsPaymentConfirmation,
      }) async {
        log(
          'Description: $description, Status Code: $statusCode, Event: $event, NeedsPaymentConfirmation: $needsPaymentConfirmation',
        );
        khalti.close(context);
      },
      onReturn: () => log('Successfully redirected to return_url.'),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: FutureBuilder(
          future: khalti,
          initialData: null,
          builder: (context, snapshot) {
            final khaltiSnapshot = snapshot.data;
            if (khaltiSnapshot == null) {
              return const CircularProgressIndicator.adaptive();
            }
            return Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Image.asset('assets/seru.png', height: 200, width: 200),
                const SizedBox(height: 120),
                const Text('Rs. 22', style: TextStyle(fontSize: 25)),
                const Text('1 day fee'),
                OutlinedButton(
                  onPressed: () => khaltiSnapshot.open(context),
                  child: const Text('Pay with Khalti'),
                ),
                const SizedBox(height: 120),
                paymentResult == null
                    ? Text('pidx: $pidx', style: const TextStyle(fontSize: 15))
                    : Column(
                      children: [
                        Text('pidx: ${paymentResult!.payload?.pidx}'),
                        Text('Status: ${paymentResult!.payload?.status}'),
                        Text(
                          'Amount Paid: ${paymentResult!.payload?.totalAmount}',
                        ),
                        Text(
                          'Transaction ID: ${paymentResult!.payload?.transactionId}',
                        ),
                      ],
                    ),
                const SizedBox(height: 120),
                const Text(
                  'This is a demo application developed by some merchant.',
                  style: TextStyle(fontSize: 12),
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}
