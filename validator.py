import os
import subprocess
from pathlib import Path

def validate_rules_files(base_folder="rules_downloads"):
    """
    Recursively find and validate all .rules files using Suricata.
    Prints files that cause errors.
    """
    # Convert to Path object for easier handling
    base_path = Path(base_folder)
    
    if not base_path.exists():
        print(f"Error: Folder '{base_folder}' does not exist!")
        return
    
    # Find all .rules files recursively
    rules_files = list(base_path.rglob("*.rules"))
    
    if not rules_files:
        print(f"No .rules files found in '{base_folder}'")
        return
    
    print(f"Found {len(rules_files)} .rules file(s). Starting validation...\n")
    
    error_files = []
    success_count = 0
    
    for rules_file in rules_files:
        try:
            # Run suricata validation
            result = subprocess.run(
                ["suricata", "-T", "-S", str(rules_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Check return code (1 means error)
            if result.returncode == 1:
                error_files.append({
                    'file': str(rules_file),
                    'stderr': result.stderr,
                    'stdout': result.stdout
                })
                print(f"❌ ERROR in: {rules_file}")
                print(f"   Cause: {result.stderr.strip()[:200]}...")  # Print first 200 chars
                print()
            else:
                success_count += 1
                print(f"✓ Valid: {rules_file}")
                
        except subprocess.TimeoutExpired:
            print(f"⏱️  TIMEOUT: {rules_file}")
            error_files.append({
                'file': str(rules_file),
                'stderr': 'Validation timeout (30s)',
                'stdout': ''
            })
        except FileNotFoundError:
            print("Error: 'suricata' command not found. Please ensure Suricata is installed.")
            return
        except Exception as e:
            print(f"⚠️  EXCEPTION for {rules_file}: {str(e)}")
            error_files.append({
                'file': str(rules_file),
                'stderr': str(e),
                'stdout': ''
            })
    
    # Summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"Total files checked: {len(rules_files)}")
    print(f"Valid files: {success_count}")
    print(f"Files with errors: {len(error_files)}")
    
    if error_files:
        print("\n" + "="*60)
        print("FILES WITH ERRORS:")
        print("="*60)
        for err in error_files:
            print(f"\n📄 {err['file']}")
            print(f"   Error: {err['stderr'][:300]}")  # Limit error message length


def combine_and_validate_rules(base_folder="rules_downloads", output_file="combined_rules.rules"):
    """
    Combine all .rules files into one and validate the combined file.
    """
    base_path = Path(base_folder)
    
    if not base_path.exists():
        print(f"Error: Folder '{base_folder}' does not exist!")
        return False
    
    # Find all .rules files recursively
    rules_files = list(base_path.rglob("*.rules"))
    
    if not rules_files:
        print(f"No .rules files found in '{base_folder}'")
        return False
    
    print(f"\n{'='*60}")
    print("COMBINING ALL RULES FILES")
    print("="*60)
    print(f"Found {len(rules_files)} .rules file(s) to combine\n")
    
    # Combine all rules into one file
    try:
        with open(output_file, 'w') as outfile:
            for rules_file in rules_files:
                try:
                    with open(rules_file, 'r') as infile:
                        content = infile.read()
                        outfile.write(f"\n# ===== From: {rules_file} =====\n")
                        outfile.write(content)
                        if not content.endswith('\n'):
                            outfile.write('\n')
                    print(f"✓ Added: {rules_file}")
                except Exception as e:
                    print(f"⚠️  Could not read {rules_file}: {e}")
        
        print(f"\n✓ Combined rules written to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error writing combined file: {e}")
        return False
    
    # Validate the combined file
    print(f"\n{'='*60}")
    print("VALIDATING COMBINED RULES FILE")
    print("="*60)
    
    try:
        result = subprocess.run(
            ["suricata", "-T", "-S", output_file],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 1:
            print(f"❌ VALIDATION FAILED for combined rules file!")
            print(f"\nError output:")
            print(result.stderr)
            print(f"\nStdout:")
            print(result.stdout)
            return False
        else:
            print(f"✅ SUCCESS! Combined rules file is valid!")
            print(f"\nValidation output:")
            print(result.stdout)
            return True
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  TIMEOUT: Validation took longer than 60 seconds")
        return False
    except FileNotFoundError:
        print("Error: 'suricata' command not found. Please ensure Suricata is installed.")
        return False
    except Exception as e:
        print(f"⚠️  EXCEPTION during validation: {str(e)}")
        return False
