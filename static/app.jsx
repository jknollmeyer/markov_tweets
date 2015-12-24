var UsernameInput = React.createClass({
  getInitialState: function(){
    return {username: ''};
  },
  handleUsernameChange: function(e){
    this.setState({username: e.target.value});
  },
  handleSubmit: function(e){
    e.preventDefault();
    this.state.data = 'Loading....';
    var username = this.state.username.trim();
    if(!username){
      return;
    }
    $.ajax({
      url: "http://localhost:5000/tweets",
      type: 'POST',
      data: {username: username},
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err){
        console.error(status, err.toString());
      }.bind(this)
    });
    this.setState({username: ''});
  },
  render: function(){
    return (
      <div>
        <form className="usernameForm" onSubmit={this.handleSubmit}>
          <input
            type="text"
            placeholder="Twitter username"
            value={this.state.username}
            onChange={this.handleUsernameChange}
          />
        <input type="submit" value="Generate" />
        </form>
        <p>{this.state.data}</p>
    </div>
    );
  }
});


ReactDOM.render(
  <UsernameInput />,
  document.getElementById('twitter_login')
);
