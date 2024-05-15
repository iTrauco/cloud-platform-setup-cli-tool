import boto3
import pandas as pd
import click

def get_all_aws_services():
    # Initialize the Boto3 client for the AWS Marketplace Catalog API
    client = boto3.client('marketplace-catalog', region_name='us-east-1')  # Specify the AWS region
    
    # Get all available products from the Marketplace Catalog API
    products_info = []
    paginator = client.get_paginator('list_entities')
    for page in paginator.paginate(Catalog='AWSMarketplace'):
        for product in page['EntitySummaryList']:
            product_name = product.get('Name')
            if product_name:
                products_info.append({'Product Name': product_name})
    
    # Extract unique service names from product names
    service_names = set()
    for product_info in products_info:
        product_name = product_info['Product Name']
        service_name = product_name.split(':')[0]  # Assuming service names are before the first ':'
        service_names.add(service_name)
    
    # Construct service information
    services_info = [{'Service Name': service_name, 'Description': 'AWS Service'} for service_name in service_names]
    
    return services_info

@click.command()
def main():
    """
    This script retrieves information about AWS services and outputs it to a CSV file.
    """
    click.echo("Welcome to the Cloud Services CLI!")
    cloud_provider = click.prompt("Which cloud provider's services do you want to retrieve? (aws/gcp/azure)", type=str)

    if cloud_provider.lower() == 'aws':
        click.echo("Retrieving information about AWS services...")
        services_info = get_all_aws_services()
        output_dir = 'Data'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'aws_services.csv')
        df = pd.DataFrame(services_info)
        df.to_csv(output_path, index=False)
        click.echo(f"Output saved to {output_path}")
    elif cloud_provider.lower() == 'gcp':
        click.echo("Retrieving information about GCP services...")
        # Call function to retrieve GCP services
        # save_to_csv(gcp_services_info, output)
        click.echo("GCP services retrieval is not implemented yet.")
    elif cloud_provider.lower() == 'azure':
        click.echo("Retrieving information about Azure services...")
        # Call function to retrieve Azure services
        # save_to_csv(azure_services_info, output)
        click.echo("Azure services retrieval is not implemented yet.")
    else:
        click.echo("Invalid input. Please choose either 'aws', 'gcp', or 'azure'.")

if __name__ == "__main__":
    main()

