var UsernameInput = React.createClass({
  getInitialState: function(){
    return {username: ''};
  },
  handleUsernameChange: function(e){
    this.setState({username: e.target.value});
  },
  resetTweet: function(e){
    this.setState({responseSuccess: false});
  },
  handleSubmit: function(e){
    e.preventDefault();
    this.setState({pageData: 'Loading...', loading: true, responseSuccess: false, status: ''});
    var username = this.state.username.trim();
    if(!username){
      this.setState({pageData: "Please enter a username" });
      return;
    }

    $.ajax({
      url: "http://localhost:5000/tweets",
      type: 'POST',
      dataType: 'json',
      data: {username: username},
      success: function(data) {
        //Catch a 404 from the API call, which should be caused by invalid user
        if (data == '404') this.setState({status: 'Username entered was invalid', loading: false, pageData: ''});
        //Catchall for all other HTTP errors
        else if(data == 'UNKNOWN') this.setState({status: 'Unknown error', loading: false, pageData: ''});
        //Save the generated tweet text and record a successful response
        else this.setState({
          pageData: data.tweet,
          twitPic: data.pic,
          responseSuccess: true,
          loading: false});
      }.bind(this),
      error: function(xhr, status, err){
        console.error(status, err.toString());
      }.bind(this)
    });
  },


  render: function(){
    var partial;
    //If we generate a tweet, partial becomes a twitter card
    if(this.state.responseSuccess || this.state.loading){
      partial = (
        <div>
          <blockquote className="twitter-tweet">
            <img src={this.state.twitPic}/>
            <span>@{this.state.username}</span>
            <p>{this.state.pageData}</p>
          </blockquote>
          <div>
            <button type="button" className="btn btn-default"
               onClick={this.handleSubmit}>
              Regenerate Tweet</button>
            <button type="button" className="btn btn-default"
              onClick={this.resetTweet}>
              Try a different account
            </button>
          </div>
        </div>


      )
    }else{
      partial = (
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
          <p>{this.state.status}</p>
      </div>
      )
    }

    return (
      partial
    );
  }
});


ReactDOM.render(
  <UsernameInput />,
  document.getElementById('twitter_login')
);
