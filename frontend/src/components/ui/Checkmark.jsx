const Checkmark = ({ checked }) => {
  return <span className={checked ? 'text-success' : 'text-danger'}>{checked ? '✓' : '✗'}</span>;
};

export default Checkmark;
