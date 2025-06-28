const Checkmark = ({ checked, title }) => {
  console.log(title, 'is', checked);
  return <span className={checked ? 'text-success' : 'text-danger'}>{checked ? '✓' : '✗'}</span>;
};

export default Checkmark;
