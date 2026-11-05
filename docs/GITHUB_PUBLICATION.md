# Publish LAB-11 to GitHub from Windows — one ZIP

**Target:** `https://github.com/r3eskelsen/eskelsen-business-website-demo`  
**Visibility:** public  
**Repository contents:** code + docs + sanitized synthetic evidence, not production credentials or real customer data.

1. Extract the provided all-in-one ZIP into a **new empty local folder** (not your current project folder). Its internal folder is `eskelsen-business-website-demo`.
2. Install **Git for Windows** and **GitHub CLI (`gh`)** if they are not installed. Authenticate: `gh auth login` (select GitHub.com and browser). If needed, run `gh auth setup-git` to let Git use GitHub CLI credentials.
3. In PowerShell, `cd` into the extracted `eskelsen-business-website-demo` folder (the one with `README.md` and `scripts`).
4. Run `& .\scripts\PUBLISH_TO_GITHUB.ps1`.
5. The script hashes every file in the public manifest, checks for common forbidden files and does **not** overwrite a remote repository with existing commits. It then creates an empty public repository if missing, commits the public files and pushes to `main`.
6. Confirm the GitHub URL shows the four-page source, `LICENSE`, evidence and README. The script reports success only if the push returns success.

### Important restrictions

- **Do not upload the ZIP as a lone repository file**; upload the extracted contents. The ZIP is a delivery container, not the source-tree format GitHub should display.
- Do not run the script from `D:\Demo_Projects\eskelsen-business-website-demo` if that folder contains pre-existing private/test data. Use the clean extracted folder.
- No force pushes, deleting repositories, changing existing branches or rewriting history. If the target repo already contains files/commits, this script stops; examine the repo manually instead of overriding it.
- Only publish code/assets for which you have permission. The license in this release is MIT.
- A clean public repo does not mean the code is a live production website or that WCAG certification was performed.

### Command example

```powershell
# After extracting the ZIP, change this path to the clean extracted folder.
Set-Location 'D:\Demo_Projects\LAB11_GITHUB_RELEASE\eskelsen-business-website-demo'
& .\scripts\PUBLISH_TO_GITHUB.ps1
```

If PowerShell's execution policy prevents running `.ps1`, use a process-scoped setting after reviewing the script: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and then rerun. Never change machine-wide policy for this release.
