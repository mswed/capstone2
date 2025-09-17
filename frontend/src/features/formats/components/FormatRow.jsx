import { Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import Checkmark from "../../../components/ui/Checkmark";
import VoteWidget from "./VoteWidget";

const FormatRow = ({
  format,
  showModel = true,
  showAddButton = false,
  onFormatAdd,
  onVote,
}) => {
  const handleAdd = () => {
    if (onFormatAdd) {
      onFormatAdd(format.id);
    }
  };

  return (
    <tr>
      {showModel && <td>{format.makeName}</td>}
      {showModel && <td>{format.cameraModel}</td>}
      <td>
        {format.imageFormat} {format.imageAspect} {format.formatName}
      </td>
      <td>
        {format.imageWidth} x {format.imageHeight}
      </td>
      <td>
        {format.sensorWidth}mm x {format.sensorHeight}mm
      </td>
      <td>{format.pixelAspect}</td>
      <td className="text-center">
        <Checkmark checked={format.isAnamorphic} title="anamorphic?" />
      </td>
      <td className="text-center">
        <Checkmark checked={format.isDesqueezed} title="desqueezed?" />
      </td>
      {onVote && (
        <td>
          <VoteWidget
            formatId={format.id}
            upVotes={format.upVotes}
            downVotes={format.downVotes}
            userVote={format.userVote}
            onVote={onVote}
          />
        </td>
      )}
      <td>
        {showAddButton ? (
          <Button variant="outline-danger" size="sm" onClick={handleAdd}>
            Add
          </Button>
        ) : (
          <Link
            to={`/formats/${format.id}`}
            className="btn btn-outline-primary btn-sm"
          >
            View
          </Link>
        )}
      </td>
    </tr>
  );
};

export default FormatRow;
