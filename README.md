Deployed at: http://18.212.95.248:8000/
Please Reach out to this email if any issues with signup: nikhilsmankani@gmail.com

## 🌱 Inspiration

Agriculture faces immense challenges today — from unpredictable climate changes to crop diseases that threaten yields. We wanted to harness the power of AI to empower farmers with insights and tools that help them make informed, data-driven decisions. Our vision for FarmGen is to provide farmers with real-time, easy-to-use AI support to boost productivity, manage crop health, and ultimately contribute to global food security. 🌍

## 🌾 What it does

FarmGen is a comprehensive AI assistant designed to support farmers in three critical areas:
1. **Best Practices Guidance** – Farmers can ask for best practices on specific crops, receiving tailored advice based on an extensive knowledge base.
2. **Crop Recommendation** – Based on a farmer's location and climate data, FarmGen recommends the most suitable crops to plant for optimal yield.
3. **Disease Detection** – Farmers can upload images of diseased crops, and FarmGen will identify the issue and suggest remedies, with options for multilingual text and audio support.

In short, FarmGen brings the power of cutting-edge AI to farmers, helping them grow smarter! 🌟

## 🛠 How we built it

FarmGen is built using an advanced AI architecture that includes:
- **LangChain Agent**: Acts as the central hub, interpreting user queries and managing workflows.
- **MongoDB for Vector Search**: Powers our fast, relevant search functionality for both text and image embeddings.
- **Bedrock Claude 3 Sonnet**: Provides natural language responses that are insightful and easy to understand.
- **AWS Sagemaker**: Runs the crop recommendation model, using climate data to suggest the best crops.
- **AWS Polly**: Converts text responses to audio, allowing multilingual support for farmers across diverse regions.

We combined these components to create a system that is scalable, efficient, and user-friendly for farmers, no matter where they are.

## 🚧 Challenges we ran into

Building FarmGen was no small feat! Some of the key challenges we faced included:
- **Integrating Different AI Models**: We had to carefully design the architecture to ensure each AI component works seamlessly with the others.
- **Handling Diverse Data Types**: From image embeddings to climate data, managing various data sources was challenging but essential for providing accurate recommendations.
- **Optimizing for Multilingual Support**: Ensuring that audio and text outputs work smoothly in multiple languages was crucial for accessibility but technically complex.

Each challenge pushed us to be creative and problem-solve, helping us create a more robust and inclusive solution.

## 🎉 Accomplishments that we're proud of

We’re incredibly proud of:
- **Creating an End-to-End AI Solution**: FarmGen is a complete platform that combines real-time AI with a user-friendly interface.
- **Multilingual and Multimodal Support**: Farmers can interact with FarmGen in multiple languages and via text or audio, making it accessible to a wider audience.
- **Empowering Farmers with AI**: FarmGen is not just about technology; it’s about making a real impact in the lives of farmers by simplifying decision-making and enhancing productivity.

## 📚 What we learned

This project taught us a lot about building complex AI systems for real-world applications:
- **The Importance of Seamless Integration**: AI tools are powerful, but their impact is maximized when they’re integrated effectively.
- **User-Centric Design**: Developing for farmers taught us the value of simplicity and clarity in AI responses, especially for non-technical users.
- **Challenges of Multilingual and Audio Outputs**: We gained experience in deploying AI models that are accessible in diverse languages and formats, which is critical for global reach.

## 🚀 What's next for FarmGen

We’re excited to keep growing FarmGen with features that make a difference:
- **Enhanced Disease Database**: Expanding our disease database to cover more crops and pests.
- **Real-Time Weather Integration**: Integrating live weather data for even more accurate crop and disease recommendations.
- **Mobile App Launch**: Developing a mobile app for easier access and offline functionality.
- **Farmer Community Platform**: Building a feature where farmers can share insights and tips with each other, powered by AI insights.

FarmGen has just begun its journey, and we’re thrilled to see how it can revolutionize farming with AI! 🚜🌾
