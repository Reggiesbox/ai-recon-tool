# GitHub Setup Instructions

Your repository has been initialized locally. Follow these steps to upload it to GitHub:

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **+** icon in the top right → **New repository**
3. Repository name: `ai-recon-tool` (or your preferred name)
4. Description: "AI-powered web interface for penetration testing and reconnaissance"
5. Choose **Public** or **Private**
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click **Create repository**

## Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these commands:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ai-recon-tool.git

# Rename main branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Alternative: Using SSH (if you have SSH keys set up)

```bash
git remote add origin git@github.com:YOUR_USERNAME/ai-recon-tool.git
git branch -M main
git push -u origin main
```

## Step 3: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. The README.md will display automatically

## Updating Your Git Configuration (Optional)

If you want to set your actual name and email:

```bash
git config --global user.name "Reggiesbox"
git config --global user.email "Regina.Vasquez7099@coyote.csusb.edu"
```

Then update the last commit:
```bash
git commit --amend --reset-author
git push -f origin main
```

## Future Updates

To push future changes:

```bash
git add .
git commit -m "Your commit message"
git push
```

## Repository Settings to Consider

1. **Topics**: Add topics like `penetration-testing`, `security`, `reconnaissance`, `metasploit`, `nmap`
2. **Description**: Update repository description
3. **Website**: If you deploy the app, add the URL
4. **License**: Already set to MIT License

## Security Note

⚠️ **Important**: This repository contains security testing tools. Consider:
- Making it **Private** if you don't want it publicly visible
- Reviewing `.gitignore` to ensure no sensitive files are committed
- Never commit actual hash files, credentials, or scan results

