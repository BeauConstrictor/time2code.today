#!/usr/bin/env python3

from git_filter_repo import FilterRepo

def update_commit(commit):
    if commit.author_name == b"Bobson Tobson":
        commit.author_name = b"BeauConstrictor"
    if commit.author_email == b"dobbob11@duck.com":
        commit.author_email = b"scabby-gone-boring@duck.com"
    if commit.committer_name == b"Bobson Tobson":
        commit.committer_name = b"BeauConstrictor"
    if commit.committer_email == b"dobbob11@duck.com":
        commit.committer_email = b"scabby-gone-boring@duck.com"

repo = FilterRepo()
repo.add_commit_callback(update_commit)
repo.run()
