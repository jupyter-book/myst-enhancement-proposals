import { readFileSync, readdirSync, statSync } from 'fs';
import { join } from 'path';
import yaml from 'js-yaml';

function getTableData(meps = 'meps') {
  let table = [];

  const readDirectoryRecursively = (directory) => {
    let results = [];
    const list = readdirSync(directory);

    list.forEach((file) => {
      const filePath = join(directory, file);
      const stat = statSync(filePath);

      if (stat && stat.isDirectory()) {
        results = results.concat(readDirectoryRecursively(filePath));
      } else {
        results.push(filePath);
      }
    });

    return results;
  };

  const mepFiles = readDirectoryRecursively(meps).filter((file) => file.includes('mep-'));

  mepFiles.forEach((imep) => {
    const text = readFileSync(imep, 'utf-8');
    const data = text.split('---')[1].trim();
    const parsedYaml = yaml.load(data);

    const tablemd = {};
    tablemd.label = parsedYaml['label'].replace('MEP', '');
    tablemd.title = parsedYaml['title'];
    tablemd.date = parsedYaml['date'];
    tablemd.status = parsedYaml['tags'][0];
    tablemd.discussion = parsedYaml['data']['discussion'];

    table.push(tablemd);
  });
  return table;
}

function cell(child) {
  if (child.type === 'tableCell') return child;
  const tableCell = {
    type: 'tableCell',
    children: typeof child === 'string' ? [{ type: 'text', value: child }] : child,
  };
  return tableCell;
}

function row(children, header = false) {
  const tableRow = {
    type: 'tableRow',
    children: children.map(cell),
  };
  if (header) {
    tableRow.children.forEach((node) => {
      node.header = true;
    });
  }
  return tableRow;
}

function getColor(tag) {
  switch (tag.toLowerCase()) {
    case 'active':
      return '#6398B6';
    case 'accepted':
      return '#3E872C';
    case 'not accepted':
      return '#D83C6E';
    case 'draft':
    default:
      return '#B1B0AF';
  }
}

function createTableRow(data) {
  return row([
    cell(data.label),
    cell([
      {
        type: 'link',
        url: `/mep-${data.label}`,
        internal: true,
        dataUrl: `/mep-${data.label}.json`,
        children: [{ type: 'text', value: data.title }],
      },
    ]),
    cell(data.date),
    cell([
      {
        type: 'span',
        class: 'shadow text-xs',
        style: {
          backgroundColor: getColor(data.status),
          color: 'white',
          padding: '5px 7px',
          borderRadius: 10,
        },
        children: [{ type: 'text', value: data.status }],
      },
    ]),
    cell([
      {
        type: 'link',
        url: data.discussion,
        children: [{ type: 'text', value: `#${data.discussion.split('/pull/')[1]}` }],
      },
    ]),
  ]);
}

const mepTable = {
  name: 'mep-table',
  doc: 'Show the MEPs as a list',
  // arg: { type: String, doc: '' },
  // options: {
  //   size: { type: String, doc: '' },
  // },
  run(data) {
    const table = getTableData();
    return [
      {
        type: 'table',
        children: [
          row(['Number', 'Title', 'Created', 'Status', 'Discussion'], true),
          ...table.map(createTableRow),
        ],
      },
    ];
  },
};

const plugin = { name: 'MyST Extension Proposal Helpers', directives: [mepTable] };

export default plugin;
