<template>
  <mu-col span="9" xl="9">
    <mu-container><div v-for="person in person_books.reader" v-bind:key="person.id">
      <h3>Читатель {{person.full_name}}</h3>
      <mu-row>
        <mu-col span="1"></mu-col>
        <mu-col justify-content="end">
          <mu-flex>Номер читательского билета: {{person.library_card_num}}</mu-flex>
          <mu-flex>Зал: {{person.hall}}</mu-flex>
          <mu-flex>Адрес: {{person.home_address}}</mu-flex>
          <mu-flex>Паспортные данные: {{person.passport_data}}</mu-flex>
        </mu-col>
        <mu-col justify-content="end">
          <mu-flex>Дата рождения: {{person.birth_date}}</mu-flex>
          <mu-flex>Контактный номер: {{person.phone_num}}</mu-flex>
          <mu-flex>Образование: {{person.education}}</mu-flex>
          <mu-flex v-if="person.degree">Имеется учёная степень</mu-flex>
          <mu-flex v-else>Отсутствует учёная степень</mu-flex>
        </mu-col>
      </mu-row>
      <mu-flex><hr/></mu-flex>
      <mu-flex justify-content="end">
        <mu-button color="indigo400" @click="changeReader(person_books.reader[0])" small>
          Изменить данные о читателе
        </mu-button>
      </mu-flex>
      <mu-flex><h4>Закреплённые за читателем в данный момент книги:</h4></mu-flex>
    </div>
    <div v-for="book in person_books.books" v-bind:key="book.book.cipher">
      <mu-row>
        <mu-col span="1"><strong>{{book.book.cipher}}</strong></mu-col>
        <mu-col>
          <mu-flex class="title">Книга: {{book.book.title}}</mu-flex>
          <mu-flex>Автор: {{book.book.author}}</mu-flex>
          <mu-flex>Зал: {{book.book.hall}}</mu-flex>
          <mu-flex>Дата закрепления: {{book.attachment_starting_date}}</mu-flex>
          <mu-flex justify-content="end">
            <mu-form :model="detachment_form[book.book.id]" class="detachment-form"
                     :label-position="labelPosition" label-width="150">
              <mu-form-item prop="date" label="Дата открепления" help-text="В формате: год(4 цифры)-месяц-день">
                <mu-text-field v-model="detachment_form[book.book.id].date"></mu-text-field>
              </mu-form-item>
            </mu-form>
            <mu-button color="error"
                       @click="detach(idAtt=book.id, idForm=book.book.id)">
              Открепить
            </mu-button>
          </mu-flex>
        </mu-col>
      </mu-row>
      <mu-row><mu-flex><hr/></mu-flex></mu-row>
    </div>
    <mu-row>
      <mu-flex><strong>Добавить новое закрепление книги за данным читателем:</strong></mu-flex>
    </mu-row>
    <mu-row>
      <mu-form :model="form" class="mu-demo-form" :label-position="labelPosition" label-width="150">
        <mu-form-item prop="input" label="Шифр книги">
          <mu-text-field v-model="form.input"></mu-text-field>
        </mu-form-item>
        <mu-form-item prop="date" label="Дата закрепления" help-text="В формате: год(4 цифры)-месяц-день">
          <mu-text-field v-model="form.date"></mu-text-field>
        </mu-form-item>
        <mu-form-item>
          <mu-button color="primary" @click="addAtt">Добавить</mu-button>
        </mu-form-item>
      </mu-form>
    </mu-row></mu-container>
  </mu-col>
</template>

<script>
export default {
  name: 'Reader_books',
  props: {
    id: ''
  },
  data () {
    return {
      person_books: '',
      labelPosition: 'left',
      book_form: '',
      form: {
        input: '',
        date: ''
      },
      detachment_form: []
    }
  },
  created () {
    // eslint-disable-next-line
    $.ajaxSetup({
      headers: {'Authorization': 'Token ' + sessionStorage.getItem('auth_token')}
    })
    this.loadBooks()
  },
  methods: {
    loadBooks () {
      // eslint-disable-next-line
      $.ajax({
        url: 'http://127.0.0.1:8000/api/lib/reader/',
        type: 'GET',
        data: {
          reader: this.id
        },
        success: (response) => {
          this.person_books = response.data
          let idList = []
          for (let j = 0; j < this.person_books.books.length; j++) {
            idList.push(this.person_books.books[j].book.id)
          }
          let maxNum = Math.max(...idList)
          for (let i = 0; i < maxNum + 1; i++) {
            this.detachment_form.push({attachment: '', date: ''})
          }
        }
      })
    },
    addAtt () {
      // eslint-disable-next-line
      $.ajax({
        url: 'http://127.0.0.1:8000/api/lib/book/',
        type: 'GET',
        data: {
          book: this.form.input
        },
        success: (response) => {
          if (response.data.length !== 0) {
            this.book_form = response.data[0].id
            // eslint-disable-next-line
            $.ajax({
              url: 'http://127.0.0.1:8000/api/lib/reader/',
              type: 'POST',
              data: {
                reader: this.id,
                book: this.book_form,
                attachment_starting_date: this.form.date
              },
              success: (response) => {
                alert('Закрепление добавлено')
                this.form.input = ''
                this.form.date = ''
                this.loadBooks()
              },
              error: (response) => {
                alert('Error')
              }
            })
          } else {
            alert('Книга с введённым шифром отсутствует в библиотеке')
          }
        },
        error: (response) => {
          alert('Error')
        }
      })
    },
    detach (idAtt, idForm) {
      this.detachment_form[idForm].attachment = idAtt
      let data = {
        data: {
          type: 'Attachment',
          id: idAtt,
          attributes: {
            attachment_finishing_date: this.detachment_form[idForm].date
          }
        }
      }
      fetch(`http://127.0.0.1:8000/api/lib/detach/${this.detachment_form[idForm].attachment}/`,
        {
          method: 'PUT',
          headers: {
            'Authorization': 'Token ' + sessionStorage.getItem('auth_token'),
            'Content-Type': 'application/vnd.api+json'
          },
          body: JSON.stringify(data)
        }
      ).then(response => {
        alert('Книга успешно откреплена')
        this.loadBooks()
      })
    },
    changeReader (person) {
      this.$router.push({name: 'reader_change', params: {person}})
    }
  }
}
</script>

<style scoped>
  .mu-demo-form {
    width: 100%;
    max-width: 460px;
  }
  .title {
    text-align: justify;
  }
  .detachment-form {
    width: 400px;
    height: 50px;
  }
</style>
