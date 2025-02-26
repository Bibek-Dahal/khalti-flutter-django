import 'package:flutter/material.dart';
import 'package:payment_demo/model/Plants.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:payment_demo/screens/KhaltiDemo.dart';

class PlantsListScreen extends StatelessWidget {
  final List<Plant> plants = [
    Plant(
      id: 1,
      name: "Aloe Vera",
      imageUrl: "assets/images/aloe_vera.jpg",
      price: 12.99,
    ),
    Plant(
      id: 2,
      name: "Fiddle Leaf Fig",
      imageUrl: "assets/images/peace_lily.jpg",
      price: 29.99,
    ),
    Plant(
      id: 3,
      name: "Snake Plant",
      imageUrl: "assets/images/snake_plant.jpg",
      price: 19.99,
    ),
    Plant(
      id: 4,
      name: "Peace Lily",
      imageUrl: "assets/images/peace_lily.jpg",
      price: 15.99,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          "Plants Shop",
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        backgroundColor: Colors.green,
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: ListView.builder(
          itemCount: plants.length,
          itemBuilder: (context, index) {
            final plant = plants[index];
            return Card(
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              elevation: 4,
              margin: EdgeInsets.symmetric(vertical: 8),
              child: ListTile(
                contentPadding: EdgeInsets.all(10),
                leading: ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: Image.asset(
                    plant.imageUrl,
                    width: 60,
                    height: 60,
                    fit: BoxFit.cover,
                  ),
                ),
                title: Text(
                  plant.name,
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                subtitle: Text(
                  "\$${plant.price.toStringAsFixed(2)}",
                  style: TextStyle(fontSize: 16, color: Colors.green),
                ),
                trailing: ElevatedButton(
                  onPressed: () async {
                    var url = Uri.parse(
                      "http://192.168.1.67:8000/orders/khalti-initiate/",
                    );

                    var payload = {
                      "return_url":
                          "http://192.168.1.67:8000/orders/khalti-verify/",
                      "website_url": "http://192.168.1.67:8000",
                      "price": plant.price * 1000,
                      "quantity": 12,
                      "name": plant.name,
                      "user_id": 1,
                      "phone_number": "9866666666",
                    };

                    print("hello");
                    try {
                      var response = await http.post(
                        url,
                        headers: {"Content-Type": "application/json"},
                        body: jsonEncode(payload),
                      );
                      print("response===${response}");

                      if (response.statusCode == 200) {
                        var responseData = jsonDecode(response.body);
                        print("$responseData");
                        Uri uri = Uri.parse(responseData['redirect_url']);
                        String? pidx = uri.queryParameters['pidx'];
                        print("pidx====,$pidx");
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => KhaltiSDKDemo(pidx: pidx!),
                          ),
                        );
                      } else {
                        throw Exception("Failed to initiate payment");
                      }
                    } catch (err) {
                      print("Error: $err");
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text("Payment initiation failed!")),
                      );
                    }
                  },

                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                  ),
                  child: Text("Buy", style: TextStyle(color: Colors.white)),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
