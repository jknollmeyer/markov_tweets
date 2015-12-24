var UsernameInput = React.createClass({
  getInitialState: function(){
    return {username: ''};
  },
  handleUsernameChange: function(e){
    this.setState({username: e.targer.value});
  },
  render: function(){
    return (
      <form className="usernameForm">
        <input
          type="text"
          placeholder="Twitter username"
          value={this.state.username}
          onChange={this.handleUsernameChange}
        />
      <input type="submit" value="Generate" />
      </form>
    );
  }
});


ReactDOM.render(
  <UsernameInput />,
  document.getElementById('twitter_login')
);
