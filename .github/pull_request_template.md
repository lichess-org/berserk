<!-- Describe your pull request here.-->


<details>
<summary>Checklist when adding a new endpoint</summary>


<!-- Once you create the PR, check off all the steps below that you have completed.
If any of these steps are not relevant or you have not completed, leave them unchecked.-->

- [ ] Added new endpoint to the `README.md`
- [ ] Ensure that my endpoint name does not repeat the name of the client. Wrong: `client.users.get_user()`, Correct: `client.users.get()`
- [ ] Typed the returned JSON using TypedDicts in `berserk/types/`, [example](https://github.com/lichess-org/berserk/blob/master/berserk/types/team.py#L32)
- [ ] Tested GET endpoints not requiring authentification. [Documentation](https://github.com/lichess-org/berserk/blob/master/CONTRIBUTING.rst#using-pytest-recording--vcrpy), [example](https://github.com/lichess-org/berserk/blob/master/tests/clients/test_teams.py#L11)
- [ ] Added the endpoint and your name to `CHANGELOG.md` in the `To be released` section (to be created if necessary)
</details>