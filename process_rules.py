import os
import tarfile
from pathlib import Path
import subprocess


def create_tarball_archives(base_folder="rules_downloads", output_folder="rules"):
    """
    Create tar.gz archives of each subfolder in rule_downloads and save to rules directory.
    """
    base_path = Path(base_folder)
    output_path = Path(output_folder)
    
    if not base_path.exists():
        print(f"Error: Folder '{base_folder}' does not exist!")
        return False
    
    # Create output directory if it doesn't exist
    output_path.mkdir(exist_ok=True)
    print(f"✓ Created/verified output directory: {output_folder}\n")
    
    print(f"{'='*60}")
    print("CREATING TAR.GZ ARCHIVES")
    print("="*60)
    
    # Get all immediate subdirectories (not recursive)
    subdirs = [d for d in base_path.iterdir() if d.is_dir()]
    
    if not subdirs:
        print(f"No subdirectories found in '{base_folder}'")
        return False
    
    print(f"Found {len(subdirs)} subfolder(s) to archive\n")
    
    success_count = 0
    failed_archives = []
    
    for subdir in subdirs:
        folder_name = subdir.name
        archive_name = f"{folder_name}.tar.gz"
        archive_path = output_path / archive_name
        
        try:
            print(f"📦 Creating archive: {archive_name}")
            
            # Create tar.gz archive
            with tarfile.open(archive_path, "w:gz") as tar:
                # Add the subfolder to the archive
                # arcname keeps the folder structure
                tar.add(subdir, arcname=folder_name)
            
            # Get archive size
            size_mb = archive_path.stat().st_size / (1024 * 1024)
            print(f"   ✓ Success! Size: {size_mb:.2f} MB")
            print(f"   Location: {archive_path}\n")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}\n")
            failed_archives.append({'folder': folder_name, 'error': str(e)})
    
    # Summary
    print("="*60)
    print("ARCHIVE CREATION SUMMARY")
    print("="*60)
    print(f"Total subfolders: {len(subdirs)}")
    print(f"Successfully archived: {success_count}")
    print(f"Failed: {len(failed_archives)}")
    
    if failed_archives:
        print("\nFailed archives:")
        for fail in failed_archives:
            print(f"  - {fail['folder']}: {fail['error']}")
    
    print(f"\n✓ All archives saved to: {output_path.absolute()}")
    return success_count > 0
