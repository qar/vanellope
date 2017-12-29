/* eslint-disable */
import CodeMirror from 'codemirror';
window.CodeMirror = CodeMirror;
import * as _ from 'lodash';
import showdown from 'showdown';
const converter = new showdown.Converter();
import apis from '@/utils/api';
import toMarkdown from 'to-markdown';

export default {
  name: 'MarkdownEditor',

  data() {
    return {
      // CodeMirror Options
      options: {
        // 编辑器模式: Github Flavor Markdown
        mode: 'gfm',

        // 是否自动折行
        lineWrapping: true,

        // 是否显示行号
        lineNumbers: false, // true or false

        // 滚动条样式
        scrollbarStyle: 'null', // native, null

        // 自动获取焦点
        autofocus: true,
      },

      // 设置选项
      settings: {
        // 文章标题
        title: '',

        select: '',
        radio: 'male',
        checkbox: [],
        switch: true,
        date: '',
        time: '',
        slider: [20, 50],
        textarea: ''
      },

      article: null,

      // in editing or in preview, or in settings
      section: 'edit',

      html: '',
    };
  },

  // boot-up
  mounted() {
    window.addEventListener('resize', this.handleResize)

    this.editor = new CodeMirror(this.$el, this.options);
    if (this.article) {
      if (this.article.ext === 'html') {
        this.editor.setValue(toMarkdown(this.article.content));
      } else {
        this.editor.setValue(this.article.content);
      }

      this.editor.refresh();
    }
    this.handleResize(); // manually called to initialize
  },

  created() {
    if (this.$route.params.articleId) {
      apis.getArticle(this.$route.params.articleId)
        .then(res => {
          this.article = res;
          this.settings.title = this.article.title;

          if (this.editor) {
            if (this.article.ext === 'html') {
              this.editor.setValue(toMarkdown(this.article.content));
            } else {
              this.editor.setValue(this.article.content);
            }

            this.editor.refresh();
            this.handleResize(); // manually called to initialize
          }
        });
    }
  },

  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
  },

  methods: {
    handleResize(ev) {
      const totalHeight = ev ? ev.target.innerHeight : (window.innerHeight - 35);
      const tabsHeight = document.getElementsByClassName('ivu-tabs-bar')[0].offsetHeight;
      const h = `${totalHeight - tabsHeight - 16}px`;
      document.getElementsByClassName('CodeMirror-scroll')[0].style.height = h;
    },

    preview() {
      // hide CodeMirror intance DOM
      const cmEle = this.editor.getWrapperElement();
      cmEle.classList.add('hide-cm-instance');

      // convert markdown to html and show on page
      const content = this.editor.getValue();
      this.html = converter.makeHtml(content);

      this.section = 'preview';
    },

    editing() {
      // show CodeMirror instance DOM
      const cmEle = this.editor.getWrapperElement();
      cmEle.classList.remove('hide-cm-instance');

      this.section = 'edit';
    },

    publish() {
      const params = {
        category: '',
        content: '',
        title: this.settings.title,
        state: 'published',
        ext: 'markdown'
      };

      params.content = this.html;

      apis.createArticle(params);
    },

    saveAsDraft() {}

  },
};
