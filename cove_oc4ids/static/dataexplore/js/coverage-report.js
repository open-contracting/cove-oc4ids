Vue.use(Fragment.Plugin);

Vue.component("tree-item", {
  template: "#item-template",
  props: ["name", "properties", "path", "search", "filter", "open", "depth"],
  components: { fragment: Fragment.Fragment },

  computed: {
    show: function () {
      // say if this row can be seen in the tree.
      return this.properties.searchMatch && this.properties.filterMatch;
    },
    showStats: function () {
      //  should the stats be displayed
      if (this.filter === "complete" && this.properties.coverage.percentage < 100) {
        return false;
      }
      if (this.filter === "incomplete" && this.properties.coverage.percentage === 100) {
        return false;
      }
      return true;
    },
    childrenOpen: function () {
      // say if the children can be seen
      if (!this.properties.hasOwnProperty("isOpen")) {
        return this.open;
      }
      return this.open && this.properties.isOpen;
    },
    subproperties: function () {
      // children properties of the array or object
      if (this.properties.hasOwnProperty("properties")) {
        return this.properties.properties;
      }
      if (this.properties.hasOwnProperty("items") && this.properties.items.hasOwnProperty("properties")) {
        return this.properties.items.properties;
      }
      return {};
    },
  },
  methods: {
    toggle: function () {
      // open or close tree node
      if (this.properties.allowOpen) {
        this.$root.openClosePath(this.path, !this.properties.isOpen);
      }
    },
    createNewPath: function (key) {
      // create path to help with opening and closing
      var newPath = this.path.slice(); //copy path
      // in the case of an array
      if (!this.properties.hasOwnProperty("properties")) {
        newPath.push("items");
      }
      newPath.push("properties", key);
      return newPath;
    },
    highlight: function (text) {
      // highlight search results
      if (!this.search) {
        return text;
      }
      return text.replace(RegExp(this.search, "gi"), function (match) {
        return '<mark class="p-0">' + match + "</mark>";
      });
    },
  },
});

var coverage = new Vue({
  el: "#coverage-report",
  template: "#coverage-template",
  data: function () {
    var termPath = [];

    var schemaData = JSON.parse(document.getElementById("field_coverage_json").textContent);
    this.augmentProperties(schemaData.properties);

    return {
      schemaData: schemaData.properties,
      termPath: termPath,
      search: "",
      filter: "all",
    };
  },
  watch: {
    search: function (newSearch) {
      this.searchAndFilter(this.schemaData, newSearch, this.filter, true, false);
    },
    filter: function (newFilter) {
      this.searchAndFilter(this.schemaData, this.search, newFilter, false, false);
    },
  },
  methods: {
    searchAndFilter: function (properties, search, filter, searchChange, objectMatch) {
      // traverse the whole jsonSchema tree to decide what nodes should be visible
      // and what objects/arrays should be open.
      var searchFound = false;
      var filterFound = false;

      for (var key in properties) {
        if (!properties.hasOwnProperty(key)) {
          continue;
        }
        var fieldProperties = properties[key];

        // match search
        var searchMatch = true;

        if (search !== "" && key.search(RegExp(this.search, "ig")) === -1) {
          searchMatch = false;
        }

        // match filter
        var filterMatch = true;

        if (filter === "complete" && fieldProperties.coverage.percentage < 100) {
          filterMatch = false;
        }
        if (filter === "incomplete" && fieldProperties.coverage.percentage === 100) {
          filterMatch = false;
        }

        var subproperties = undefined;

        if (fieldProperties.hasOwnProperty("properties")) {
          subproperties = fieldProperties.properties;
        }
        if (fieldProperties.hasOwnProperty("items") && fieldProperties.items.hasOwnProperty("properties")) {
          subproperties = fieldProperties.items.properties;
        }

        if (subproperties) {
          if (searchChange) {
            fieldProperties.isOpen = false;
          }
          children = this.searchAndFilter(subproperties, search, filter, searchChange, searchMatch || objectMatch);
          if (children.searchFound) {
            searchMatch = true;
            if (searchChange && search !== "") {
              fieldProperties.isOpen = true;
            }
          }
          if (children.filterFound) {
            filterMatch = true;
          }
          // if either search or filter is not found do not allow tree open
          // if parent object searched for allow all children to open
          if (!(children.filterFound && (children.searchFound || objectMatch || searchMatch))) {
            fieldProperties.allowOpen = false;
          } else {
            fieldProperties.allowOpen = true;
          }
        }

        fieldProperties.filterMatch = filterMatch;
        if (filterMatch) {
          filterFound = true;
        }

        fieldProperties.searchMatch = searchMatch || objectMatch;
        if (searchMatch) {
          searchFound = true;
        }
      }

      return { searchFound: searchFound, filterFound: filterFound };
    },
    openClosePath: function (path, open) {
      // given a full path open and close the tree node at that point
      var current = this.schemaData;
      for (i = 0; i < path.length; ++i) {
        current = current[path[i]];
      }
      if (!current.hasOwnProperty("isOpen")) {
        return;
      }
      if (open && !current.isOpen) {
        current.isOpen = true;
      }
      if (!open && current.isOpen) {
        current.isOpen = false;
      }
    },
    augmentProperties: function (properties) {
      // before data is passed to vue add extra fields to the raw data. These fields
      // can not be added later otherwise vue will not track their changes.
      for (var key in properties) {
        var fieldProperties = properties[key];

        var subproperties;
        var extraPath = [];

        if (fieldProperties.hasOwnProperty("properties")) {
          subproperties = fieldProperties.properties;
          extraPath = ["properties"];
        }
        if (fieldProperties.hasOwnProperty("items") && fieldProperties.items.hasOwnProperty("properties")) {
          subproperties = fieldProperties.items.properties;
          extraPath = ["items", "properties"];
        }
        // this is a proxy to saying the field is an object or array, therefore has children.
        if (extraPath.length > 0) {
          // close all by default
          fieldProperties.isOpen = false;
          fieldProperties.allowOpen = true;

          this.augmentProperties(subproperties);
        }

        fieldProperties.searchMatch = true;
        fieldProperties.filterMatch = true;
      }
    },
  },
});
