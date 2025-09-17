import { useState } from "react";
import { Form, Button, InputGroup } from "react-bootstrap";

/**
 * A search form components that runs a setState function provided by
 * the parent component. The parent component is in charge of running the
 * actual search once the search state provided is changed, but this form handles the UI
 *
 * @param {function}  search -  The setState function provided by the parent component
 * @returns {Component} - a search form with a search field and a button
 */

const RemoteSearchForm = ({ search, placeholder = "Enter search term..." }) => {
  const INITIAL_STATE = "";
  const [searchField, setSearchField] = useState(INITIAL_STATE);

  const handleChange = (evt) => {
    setSearchField(evt.target.value);
  };

  const handleSubmit = (evt) => {
    evt.preventDefault();
    search(searchField);
  };

  const handleClear = () => {
    setSearchField("");
    search("");
  };

  return (
    <Form onSubmit={handleSubmit}>
      <InputGroup className="my-3">
        <Form.Control
          placeholder={placeholder}
          onChange={handleChange}
          value={searchField}
        />
        {searchField && (
          <Button
            variant="outline-secondary"
            onClick={handleClear}
            aria-label="Clear search"
          >
            x
          </Button>
        )}
        <Button variant="primary" type="submit">
          Search!
        </Button>
      </InputGroup>
    </Form>
  );
};

export default RemoteSearchForm;
