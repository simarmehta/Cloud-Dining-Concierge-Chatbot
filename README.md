# Cloud Dining Concierge Chatbot

This project demonstrates the implementation of a **Cloud-based Dining Concierge Chatbot** designed to help users find restaurants and make reservations. The bot leverages **AWS services** like **Lex**, **Lambda**, and **DynamoDB** to provide an intelligent, scalable, and serverless chatbot solution. It is capable of interacting with users in natural language, understanding their preferences, and recommending dining options based on their location, cuisine preferences, and more.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technologies Used](#technologies-used)


## Overview

The **Cloud Dining Concierge Chatbot** allows users to interact via natural language to find restaurant recommendations. It uses **Amazon Lex** to process voice/text inputs, **AWS Lambda** for backend logic execution, and **Amazon DynamoDB** for persisting user preferences and restaurant details. This bot can be deployed in a serverless architecture on AWS, ensuring scalability and reliability.

The chatbot accepts user inputs like:
- Cuisine preferences (e.g., Italian, Mexican, Chinese)
- Location
- Dining time
- Number of people for the reservation

Based on the inputs, the chatbot searches for appropriate restaurant options and provides recommendations to the user.

## Architecture

The chatbot system is built using AWS services, allowing for a highly scalable and serverless architecture.

![Architecture Diagram](https://example.com/path/to/your/diagram.png)

1. **Amazon Lex**: The user interacts with the chatbot via Lex, which handles Natural Language Processing (NLP) and intent recognition.
2. **AWS Lambda**: Lex triggers Lambda functions to process inputs, perform business logic (search restaurants, manage reservations), and communicate with DynamoDB.
3. **Amazon DynamoDB**: Stores user information, preferences, and restaurant details.
4. **Amazon SNS (Optional)**: Send SMS notifications with restaurant details or booking confirmations.
5. **External APIs (Optional)**: Integrates with restaurant listing services (Yelp, Zomato, etc.) for retrieving real-time restaurant data.

## Features

- **Natural Language Understanding**: Utilizes Amazon Lex to handle user intents and extract relevant information.
- **Multi-turn Conversations**: Handles multi-turn dialogue to gather all the required information before making a recommendation.
- **Restaurant Recommendations**: Provides personalized restaurant suggestions based on user preferences.
- **Flexible Input Handling**: Accepts both voice and text inputs.
- **Serverless and Scalable**: Built on AWS Lambda and DynamoDB, ensuring that the bot scales automatically with user traffic.
- **SMS Notifications**: Sends SMS confirmations or details via AWS SNS (optional feature).
- **DynamoDB Integration**: Stores user sessions, preferences, and restaurant data in a NoSQL database.

## Technologies Used

- **Amazon Lex**: For building the conversational interface.
- **AWS Lambda**: For executing backend logic in response to Lex requests.
- **Amazon DynamoDB**: For storing data such as user preferences and restaurant information.
- **Amazon SNS** (optional): For sending SMS notifications to users.
- **External Restaurant APIs** (optional): Integration with APIs such as Yelp or Zomato for real-time restaurant data.
