import React from 'react';

import { ListGroup, ListGroupItem } from 'react-bootstrap';

function formatDate(dateStr) {
  let date = new Date(dateStr);

  return `${date.getMonth()}/${date.getDay()}/${date.getFullYear()}`;
}

export default function CommitList({commits}) {
  return (
      <ListGroup>
        {commits.map(commit => {
          return (
            <ListGroupItem
              key={commit.sha}
              header={commit.commit_message}>
            {commit.commit_author.name} commited on {formatDate(commit.commit_author.date)}&nbsp;
            <a href={commit.html_url} target="_blank">{commit.sha.substring(0, 8)}</a>
            </ListGroupItem>
          );
        })}
      </ListGroup>
);
}
