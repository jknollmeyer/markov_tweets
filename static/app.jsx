var UsernameInput = React.createClass({
  getInitialState: function(){
    return {username: ''};
  },
  handleUsernameChange: function(e){
    this.setState({username: e.target.value});
  },
  handleSubmit: function(e){
    e.preventDefault();
    this.setState({PageData: 'Loading....'});
    var username = this.state.username.trim();
    if(!username){
      this.setState({pageData: "Please enter a username" });
      return;
    }
    $.ajax({
      url: "http://localhost:5000/tweets",
      type: 'POST',
      data: {username: username},
      success: function(data) {
        if (data == '404'){
          data = 'Username entered was invalid';
        }else if(data == 'UNKNOWN'){
          data = 'There was an unkown error';
        }
        this.setState({pageData: data});
      }.bind(this),
      error: function(xhr, status, err){
        console.error(status, err.toString());
      }.bind(this)
    });
    this.setState({username: ''});
  },
  render: function(){
    var partial;
    if(this.state.responseSuccess){
      partial = (
        <blockquote class="twitter-tweet">
          <p>{this.state.pageData}</p>
        </blockquote>
      )
    }
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
        <p>{this.state.pageData}</p>
    </div>
    );
  }
});


ReactDOM.render(
  <UsernameInput />,
  document.getElementById('twitter_login')
);


<blockquote class="twitter-tweet">
  <p>Currently testing: jQuery and CSS animations: fly-in - </p>
      <a data-datetime="2012-12-03T18:51:11+00:00">December 3, 2012</a>

  </blockquote>
<script src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
