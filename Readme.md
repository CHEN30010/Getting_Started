# Getting started

<img width="1408" height="768" alt="Gemini_Generated_Image_oisk3poisk3poisk" src="https://github.com/user-attachments/assets/04166a7f-2aad-4350-9c54-ba46fc8aa802" />

<img width="1408" height="768" alt="Gemini_Generated_Image_psqo7vpsqo7vpsqo" src="https://github.com/user-attachments/assets/e89be895-d09e-4369-b1cc-d46cbcd519b6" />

You are going to solve a challenging and important reaction engineering problem to a high standard based on simulations programmed by your team. The following get started guidelines will help you to make progress quickly.

**Part 1: Complete this before the first tutorial**

Come to the first tutorial with your computer and all of this section completed.

Install [python](https://www.python.org/downloads/)

- add Python to your PATH and make sure pip is included. pip helps to install additional packages easily later.

Install [VS Code](https://code.visualstudio.com/download?_exp_download=fb315fc982)

Sign-up for a [GitHub account](https://github.com/signup?ref_product=github&ref_type=engagement&ref_style=text). It's free and will help your team to collaborate. Use your UCD email address. Verify your email address when prompted.

Install [git](https://github.com/git-guides/install-git). This enables source control and audit trail for your project and syncs with GitHub. Source control makes it possible for you to track changes and revert if needed. Audit trial helps to log who did what and when, a feature that is useful for many reasons including for compliance purposes, e.g. in a GMP context.

Optional, helpful: Read/ scan these intros to Git:

- [Intro](https://webtuu.com/blog/04/a-laymans-introduction-to-git)

- [Git and GitHub](https://webtuu.com/blog/04/difference-between-git-and-github)

- [Branches and merging your work](https://webtuu.com/blog/04/git-basics-branching-merging-push-to-github)

[Generate a GitHub personal access token](https://github.com/settings/apps). It's an alternative to a password and will help a lot when pushing and pulling code between local and remote.

- use the classic type and give it full "repo" access and also read:org access.

Continue with the steps below if you have time now.  Otherwise we will do them together in the first tutorial.

**Part 2: In the first tutorial**

Sign into VS Code using your GitHub account; if you have more than one GitHub account, make sure to use your UCD account for this project.

Generate some python code, e.g. using a Google search; paste it into VS Code. Save it under your name [your_name.py] and Run.

Open a Terminal window in VS Code and run your code again; usually:
```
python [your_name.py]
```

Authenticate with GitHub using the terminal and your personal access token:
```
gh auth login
```
When prompted select GitHub.com (press Enter), https and the option to paste your token (use the down arrow key to select that); then paste your token.

The following could be "eventful" with 40+ people making changes at the same time.

You will find the GitHub Copilot assistant in VS Code helpful if you get stuck; it's available in the Chat screen. Tell it what you want to do in natural language and it will help, e.g. "Push/commit my code to this public repo: https://github.com/CHEN30010/Getting_Started".

All going well, Copilot will run something like these commands (if using Copilot, you do not need to run all of these yourself right now):

- The key steps are: initializing the repo → staging and committing → authenticating → pulling remote changes → resolving divergent branches → successfully pushing
```
	1. git status — Check repository status
	2. git init — Initialize a new git repository
	3. git remote add origin https://github.com/CHEN30010/Getting_Started.git — Add remote repository
	4. git add [your filename] — Stage the file for commit
	5. git commit -m "Your comment" — Commit with message
	6. git push -u origin main — Push to remote
	7. git remote set-url origin https://github.com/CHEN30010/Getting_Started.git — Ensure HTTPS remote URL is set
	8. git pull origin main — Pull remote changes
	9. git config pull.rebase false — Configure merge strategy to use merge
	10. git pull --allow-unrelated-histories origin main — Pull and merge unrelated histories
	11. git push origin main — Final push to remote
```

Make some changes locally in your code (e.g. add or edit a comment) and push again (use the assistant, rather than typing the commands)
```
git push origin main
```

Make a branch and then make another change (use the assistant, rather than typing the commands)
```
git switch -c [your branch name] && git status --short --branch
```

Make a pull request to incorporate the change in your branch (use the assistant, rather than typing the commands)
```
gh pr create --base main --head [your branch name] --title "Your description of change" --body "More info about the change"
```

This part requires your approval and you do manually:
- Merge the change in your browser on GitHub.com (on the Pull requests tab of the repo)

Make sure you can also access your Team repository; that is where you will be saving, sharing and submitting your team code.

If you run into problems with the above, check with your fellow team members what has worked for them. If you still have problems after that, let Joe know.

You can increase your GitHub Copilot limits by verifying your student status
[here](https://github.com/settings/education/benefits). In general, you will find it more productive to use Copilot within VS Code, rather than e.g. Google AI in the browser. If/when you exceed your Copilot limits, you can fall back on using Google AI in the browser until your limits reset.
