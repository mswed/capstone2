const NoResults = ({ message }) => {
  return (
    <div className="d-flex flex-column justify-content-center align-items-center text-center">
      <h4 className="text-muted">{message}</h4>;
    </div>
  );
};

export default NoResults;
