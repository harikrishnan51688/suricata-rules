import yaml
import requests
import tarfile
import os
from pathlib import Path
from urllib.parse import urlparse


def download_file(url, destination):
    """Download a file from URL to destination."""
    print(f"Downloading: {url}")
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"  ✓ Downloaded to: {destination}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Failed to download: {e}")
        return False

def extract_tar_gz(archive_path, extract_to):
    """Extract a tar.gz archive to a directory."""
    print(f"Extracting: {archive_path}")
    try:
        with tarfile.open(archive_path, 'r:gz') as tar:
            tar.extractall(path=extract_to)
        print(f"  ✓ Extracted to: {extract_to}")
        # Remove the archive after extraction
        os.remove(archive_path)
        return True
    except Exception as e:
        print(f"  ✗ Failed to extract: {e}")
        return False

def process_yaml_sources(yaml_file, output_dir='downloads'):
    """Process YAML file and download all rule sources."""
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Load YAML file
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    
    sources = data.get('sources', {})
    
    for source_name, source_info in sources.items():
        print(f"\n{'='*60}")
        print(f"Processing: {source_name}")
        print(f"{'='*60}")
    
        
        url = source_info.get('url')
        if not url:
            print(f"  ⚠ No URL found")
            continue
        
        # Create folder for this source
        source_folder = output_path / source_name.replace('/', '_')
        source_folder.mkdir(exist_ok=True)
        
        # Get filename from URL
        parsed_url = urlparse(url)
        filename = Path(parsed_url.path).name
        download_path = source_folder / filename
        
        # Download the file
        if not download_file(url, download_path):
            continue
        
        # Process based on file type
        if filename.endswith('.tar.gz'):
            # Extract tar.gz archive
            extract_tar_gz(download_path, source_folder)
        elif filename.endswith('.rules') or filename.endswith('.rule'):
            print(f"  ✓ Rule file saved to: {source_folder}")
        else:
            print(f"  ℹ Unknown file type, saved to: {source_folder}")
    
    print(f"\n{'='*60}")
    print(f"All downloads completed!")
    print(f"Output directory: {output_path.absolute()}")


