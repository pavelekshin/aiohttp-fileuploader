function handler({store, container, pages, url}) {

  if (!window.Handlebars) { throw new Error('Handlebars should be loaded to document'); }

  this.store = store
  this.container = container // dom app locator
  this.pages = pages // all app pages
  this.handlers = {} // all handlers
  this.url = url
  this.render = function(template, container=null) {

          data = this.store
          if (!container) {container = this.container}

          console.log(`Rendering template ${template}  to ${container}`)

          try {
            const templateElement = document.querySelector(template);

            if (!templateElement) {
              throw new Error(`Template element ${template} not found`);
            }


            const outputElement = document.querySelector(container);

            if (!outputElement) {
              throw new Error('No element to put page into ');
            }

            var templateText = templateElement.innerHTML;
            var template = Handlebars.compile(templateText);
            var renderedHTML = template(data);

            outputElement.innerHTML = renderedHTML;

          } catch (error) {
            console.error(error);
          }
    }


  this.go = function (state) {

    if (this.pages[state]) {
      this.render("#"+state, this.container, this.store);
    } else {
      console.error(`State ${state} not found`);
    }
    this.state = state
  };


  this.payload = []
  this.addPayload = function(key){
     if (!this.store.hasOwnProperty(key)) {
        throw new Error(`Payload error: ${key} not in store`);
     } else {
        this.payload.push(key)
     }
  }

   this.addHandler = function(name, func) {
       this.handlers[name] = func
       console.log(`Handler ${name} added`)
   }

   this.run = function(name, data) {

       if (typeof this.handlers[name] !== 'function') {
          throw new Error(`Handler with name ${name} doesn't exist.`);
      }

       console.log(`Handler ${name} running`)
       func = this.handlers[name](data)
   }
}