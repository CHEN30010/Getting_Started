# Getting started

You are going to solve a challenging reaction engineering problem based on  simulations programmed by your team. The following get started guidelines will help you to make progress quickly.

**Before the first tutorial**

Install [python](https://www.python.org/downloads/)

- add Python to your PATH and make sure pip is included.

Install [VS Code](https://code.visualstudio.com/download?_exp_download=fb315fc982)

Sign-up for a [GitHub account](https://github.com/signup?ref_product=github&ref_type=engagement&ref_style=text). It's free and will help your team to collaborate. Use your UCD email address. Verify your email address when prompted.

Install [git](https://github.com/git-guides/install-git). This enables source control / audit trail for your project and syncs with GitHub.

Optional: Read/ scan these intros to Git:

- [Intro](https://webtuu.com/blog/04/a-laymans-introduction-to-git)

- [Git and GitHub](https://webtuu.com/blog/04/difference-between-git-and-github)

- [Branches and merging your work](https://webtuu.com/blog/04/git-basics-branching-merging-push-to-github)

[Generate a personal access token](https://github.com/settings/apps). It's an alternative to a password and will help a lot when pushing and pulling code between local and remote.

- give it full "repo" access and also read:org access.

**In the first tutorial**

Generate some code using a Google search; paste it into VS Code. Save under your name [your_name.py] and Run.

Open a Terminal window in VS Code and run again.

Authenticate with GitHub using the terminal and your personal access token
```
gh auth login
```

Push/commit your code to a public repo.
- The key steps are: initializing the repo → staging and committing → authenticating → pulling remote changes → resolving divergent branches → successfully pushing
```
	1. git status — Check repository status
	2. git init — Initialize a new git repository
	3. git remote add origin https://github.com/CHEN30010/Team_99_test.git — Add remote repository
	4. git add [your filename] — Stage the file for commit
	5. git commit -m "Your comment" — Commit with message
	6. git push -u origin main — Push to remote
	7. git remote set-url origin https://github.com/CHEN30010/Team_99_test.git — Ensure HTTPS remote URL is set
	8. git pull origin main — Pull remote changes
	9. git config pull.rebase false — Configure merge strategy to use merge
	10. git pull --allow-unrelated-histories origin main — Pull and merge unrelated histories
	11. git push origin main — Final push to remote
```
Make some changes locally and push again
```
git push origin main
```

Make a branch and then make another change
```
git switch -c [your branch name] && git status --short --branch
```

Make a pull request to incorporate the change in your branch
```
gh pr create --base main --head [your branch name] --title "Your description of change" --body "More info about the change"
```

Merge the change in your browser on GitHub.com
