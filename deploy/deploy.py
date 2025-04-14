from azure.ai.ml.entities import ManagedOnlineDeployment, ManagedOnlineEndpoint, CodeConfiguration, Environment, Model
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os

parent_folder = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(parent_folder, '.env')
environment_path = os.path.join(parent_folder, 'environment.yml')

load_dotenv(dotenv_path)

credential = DefaultAzureCredential()
ml_client = MLClient(credential, subscription_id="SUBSCRIPTION_ID", resource_group_name="RESOURCE_GROUP", workspace_name="WORKSPACE")

model_definition = Model(
    name="my_model",
    path="model.pkl",   
    description="recommendation model"
)

registered_model = ml_client.models.create_or_update(model_definition)
print(f"Model registered: {registered_model.name} (version: {registered_model.version})")

endpoint = ManagedOnlineEndpoint(
    name="recommendation",  
    auth_mode="key"
)

code_config = CodeConfiguration(
    code="./src",     
    scoring_script="score.py"  
)

environment = Environment(
    name="myenv",
    conda_file=environment_path  
)

# retreive model
model = registered_model

# deployment object
deployment = ManagedOnlineDeployment(
    name="recommendation-service",  
    endpoint_name=endpoint.name,
    model=model,
    code_configuration=code_config,
    environment=environment,
    instance_type="Standard_F4s",
    instance_count=1
)

# deploy
ml_client.online_endpoints.begin_create_or_update(endpoint).result()
ml_client.online_deployments.begin_create_or_update(deployment).result()

print("Deployment successful!")
