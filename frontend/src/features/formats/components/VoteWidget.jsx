const VoteWidget = ({ formatId, upVotes, downVotes, userVote, onVote }) => {
  return (
    <div className="d-flex flex-column align-items-center" style={{ minWidth: '60px' }}>
      <button
        onClick={() => onVote(formatId, 'up')}
        className="btn p-0 border-0"
        style={{
          color: '#28a745', // Always green for up votes
          fontSize: '18px',
          lineHeight: 1,
        }}
      >
        {userVote === 'up' ? '▲' : '△'}
      </button>
      <small className="text-muted my-1">{upVotes - downVotes}</small>
      <button
        onClick={() => onVote(formatId, 'down')}
        className="btn p-0 border-0"
        style={{
          color: '#dc3545', // Always red for down votes
          fontSize: '18px',
          lineHeight: 1,
        }}
      >
        {userVote === 'down' ? '▼' : '▽'}
      </button>
    </div>
  );
};

export default VoteWidget;
