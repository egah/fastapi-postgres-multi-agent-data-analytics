# POSTGRES MULTI-AGENT DATA ANALYTICS
[![Python Version](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/) [![FastAPI Version](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/) [![Poetry Version](https://img.shields.io/badge/Poetry-Latest-orange.svg)](https://python-poetry.org/) [![OpenAI](https://img.shields.io/badge/OpenAI-Latest-yellow.svg)](https://www.openai.com/) [![Autogen Version](https://img.shields.io/badge/Autogen-Latest-lightgrey.svg)](https://autogen.io/) [![Docker Version](https://img.shields.io/badge/Docker-Latest-blue.svg)](https://www.docker.com/) [![Aider](https://img.shields.io/badge/Aider-Active-brightgreen.svg)](https://www.aider.com/) [![PostgreSQL Version](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/) [![Postman](https://img.shields.io/badge/Postman-Tested-orange)](https://www.postman.com/) [![Transformers & BERT](https://img.shields.io/badge/Transformers-BERT-blue.svg)](https://github.com/yourusername/transformers-bert)







### Oreview
In this project, I created an API that used the OpenAI ChatGPT completion endpoint to transform natural language into a SQL query and return the query result. One can directly make a direct call to the OpenAI API, but the endpoints of this project have several advantages:

<ul>
<li>No need to write the prompt by yourself</li>
<li>The API contains control flows that make sure that the response of the LLM is correct</li>
<li>You are aware of the cost of each call to the API</li>

</ul>





### Tables of Contents
- [Dependencies](#dependencies)
- [Usage](#usage)
- [features](#features)
- [Improvement](#improvment)
- [Deployment](#deployment)
- [Contact Information](#contact-infrmation)


### Dependencies 
This project was build with : 
- python 3.10
- FastApi
- Poetry
- Openai 
- Autogen
- aider
- docker
- Postman
- PostgreSQL

### Usage
You can find the API documentation <a href="https://fastapi-postgres-data-analytic-70044b1de0ad.herokuapp.com/docs#/">here</a>.

### Features
This API backend followed these steps: 
<ul>
<li>Use the ChatGPT completion endpoint to transform natural language into a SQL query
</li>
<li>Instead of making a single prompt, we use Autogen to create a data analytics team. Our team has multiple agents, each with a specific role. The advantage of using Autogen is that our agents can communicate to make sure that our LLM gives the right answers every time for a specific prompt.
</li>
<li>I added an orchestrator that implements sequential flows between our agents.

</li>
<li>For each prompt, we include the definitions of all the tables (the SQL query that creates the table). This is not a suitable approach for databases with thousands of tables. To limit the number of tokens in our prompt, we only keep the most relevant tables for a specific query. To obtain the most relevant tables, I use Bert Model embeddings to compute similarities between our natural language query and the table definitions. Then, we only keep the most similar tables.
</li>
<li>Our orchestrator returns a Conversational object, with attributes like the number of tokens in a request, the price of a call to the ChatGPT API, and a list that tracks all conversations between our agents.
</li>
</ul>


### Improvement
<ul>
<li>OpenAI just released gpt4, gpt4-turbo, a new completion endpoint chat completion and assistant endpoint. In the next version of the API, I will add an assistant API endpoint.</li>
<li> Improve error handling by adding the HttpException's in the code flow.</li>
</ul>


### Deployment
I deployed this API using Heroku. Heroku is a platform-as-a-service (PAAS) solution for deploying applications. Heroku allows for three methods for application deployment:

<ul>
<li>Heroku CLI</li>
<li>GitHub</li>
<li>Container registry
</li>

</ul>
Heroku allows you to create a custom pipeline for your application. For example, you can create an automatic deploy that is triggered by a `git push` to your GitHub branch.

The API was deployed using te Docker registry method.

### Contact information
 [![all text](LinkedIn.svg)](https://www.linkedin.com/in/egahepiphane/) </a><a href="mailto:egahepiphane@gmail.com">
      <img src="https://img.shields.io/badge/SEND%20MAIL-6D4C6F?&style=for-the-badge&logo=MAIL.RU&logoColor=black">
    </a>
