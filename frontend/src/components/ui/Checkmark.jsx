const Checkmark = ({ checked, title }) => {
  return <span className={checked ? 'text-success' : 'text-danger'}>{checked ? '✓' : '✗'}</span>;
};

export default Checkmark;
