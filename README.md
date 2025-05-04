# DataHub AI

## Objective

The goal of this project is to improve data provision in the public health sector through the use of Artificial Intelligence (AI), specifically for the [Datahub](https://github.com/datasnack/datahub). We are developing a ChatBot that simplifies the exploration of and queries to data sets within the DataHub. Using AI, we enable users without deep technical knowledge – such as researchers or public health actors – to explore data using natural language.

## Installation Guide

The detailed installation guide can be found in our [User Documentation](https://github.com/benedikt-weyer/datahub-ai/wiki/User-Docs).

## Contributing and Development Environment

We welcome contributions from the community! If you are interested in assisting with the development of this project, please refer to our [Contribution Guidelines](CONTRIBUTING.md) for more information on how to get started. Details on setting up your development environment can be found in the [Developer Documentation](https://github.com/benedikt-weyer/datahub-ai/wiki/Developer-Docs).


## Team Members and Roles

Our team consists of 4 people from 3 disciplines:

-   Benedikt Weyer, Applied Computer Science, responsible for software development and architecture
-   Michael German, Computer Science of Technical Systems, responsible for software development
-   Jan Biedasiek, Computer Science of Technical Systems, responsible for testing our systems
-   Yunus Sözeri, Business Informatics, responsible for the user interface and documentation

## Design

**User Interface & System Architecture**

A key advantage of our approach is the seamless integration of the ChatBot user interface into the existing Datahub interface to ensure high usability. The design is intuitive and well-documented to enable installation and use even for less technically savvy users.

The system architecture is based on containers (e.g., Docker). This container-based division clearly separates responsibilities and connects the components via defined interfaces. This creates a modular and understandable abstraction that simplifies the further development and maintenance of the system.

The flow of a request begins at the user interface embedded in Datahub. From there, user inputs are forwarded to the backend. Various containers handle specific tasks: data storage, providing interfaces for the AI module, and processing requests through the AI module itself. The AI module analyzes the natural language request, accesses the relevant data, and performs aggregations or other calculations as needed to generate an appropriate response.

## Data Acquisition

The data used for this project comes from the Datahub, an open-source application. Specifically, we use sample data (Ghana dataset) provided through Datahub's 'Datasnack' functionality.

## Evaluation

The core component of our application is a Large Language Model (LLM) hosted locally. The ChatBot is integrated as an extension into Datahub's Django application and is accessible via its user interface. Further technical details can be found in the [Documentation](https://github.com/benedikt-weyer/datahub-ai/wiki/Documentation). The project repository is available under the MIT license. A focus of the development is on local usability; an internet connection is only required once during the initial setup.

## Known Issues

Currently, the challenge is that the LLM attempts to answer general, non-data-related questions incorrectly using SQL queries. This affects the naturalness of the interaction and potentially the robustness against incorrect or ambiguous requests.

## Future Enhancements

The following further developments are planned:

*   **Kubernetes Deployment:** Testing and full configuration for use in Kubernetes environments to improve scalability and management. Currently, further adjustments to infrastructure and resource management are necessary for this.
*   **Improved Query Processing:** Development of more flexible methods for enriching user requests with contextual information to increase the accuracy and quality of the LLM's responses.
*   **User Authentication & Session Management:** Introduction of user accounts and sessions to enable personalized interactions and context sensitivity across multiple requests. This would improve the user experience, especially for more complex analyses.
*   **Feedback Mechanism:** Implementation of a way for users to provide feedback on the quality of the answers. This feedback is intended to be used to continuously improve the LLM (online learning).
